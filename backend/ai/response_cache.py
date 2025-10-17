"""
Advanced Response Cache for ScienceGPT v3.0
High-performance caching system with intelligent key generation and TTL management
"""

import asyncio
import hashlib
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import pickle
import gzip
from pathlib import Path

from .llm_handler import LLMResponse, LLMProvider
from ..config import get_settings


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    response: LLMResponse
    created_at: datetime
    accessed_at: datetime
    access_count: int
    ttl_seconds: int
    compressed: bool
    size_bytes: int


class ResponseCache:
    """Advanced caching system for LLM responses"""
    
    def __init__(self):
        """Initialize response cache"""
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        
        # Cache storage
        self.cache: Dict[str, CacheEntry] = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_entries": 0,
            "total_size_bytes": 0
        }
        
        # Cache configuration
        self.max_entries = 10000
        self.max_size_mb = 500
        self.default_ttl = self.settings.cache_ttl
        self.compression_threshold = 1024  # Compress entries > 1KB
        
        # Start background maintenance
        if self.settings.enable_caching:
            asyncio.create_task(self._maintenance_loop())
    
    def _generate_cache_key(self, question: str, context: Dict[str, Any]) -> str:
        """Generate consistent cache key from question and context"""
        
        # Extract relevant context for key generation
        key_context = {
            "question": question.lower().strip(),
            "grade": context.get("grade", 6),
            "subject": context.get("subject", "Science"),
            "language": context.get("language", "English"),
            "type": context.get("type", "general"),
            "include_examples": context.get("include_examples", True)
        }
        
        # Create deterministic key
        key_string = json.dumps(key_context, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()[:32]
    
    async def get(self, question: str, context: Dict[str, Any]) -> Optional[LLMResponse]:
        """Get cached response if available and valid"""
        
        if not self.settings.enable_caching:
            return None
        
        key = self._generate_cache_key(question, context)
        
        if key not in self.cache:
            self.cache_stats["misses"] += 1
            return None
        
        entry = self.cache[key]
        
        # Check TTL
        if self._is_expired(entry):
            await self._remove_entry(key)
            self.cache_stats["misses"] += 1
            return None
        
        # Update access information
        entry.accessed_at = datetime.now()
        entry.access_count += 1
        
        # Create response with cache flag
        response = entry.response
        response.cached = True
        
        self.cache_stats["hits"] += 1
        self.logger.debug(f"Cache hit for key: {key[:8]}...")
        
        return response
    
    async def set(self, question: str, context: Dict[str, Any], response: LLMResponse) -> bool:
        """Cache response with intelligent TTL and compression"""
        
        if not self.settings.enable_caching:
            return False
        
        key = self._generate_cache_key(question, context)
        
        # Determine TTL based on response type and quality
        ttl = self._calculate_ttl(context, response)
        
        # Serialize and optionally compress response
        data = pickle.dumps(response)
        compressed = False
        
        if len(data) > self.compression_threshold:
            data = gzip.compress(data)
            compressed = True
        
        # Create cache entry
        entry = CacheEntry(
            key=key,
            response=response,
            created_at=datetime.now(),
            accessed_at=datetime.now(),
            access_count=1,
            ttl_seconds=ttl,
            compressed=compressed,
            size_bytes=len(data)
        )
        
        # Check cache limits before adding
        if await self._check_and_enforce_limits():
            self.cache[key] = entry
            self.cache_stats["total_entries"] += 1
            self.cache_stats["total_size_bytes"] += entry.size_bytes
            
            self.logger.debug(f"Cached response for key: {key[:8]}... (TTL: {ttl}s)")
            return True
        
        return False
    
    def _calculate_ttl(self, context: Dict[str, Any], response: LLMResponse) -> int:
        """Calculate TTL based on context and response characteristics"""
        
        base_ttl = self.default_ttl
        
        # Adjust TTL based on content type
        content_type = context.get("type", "general")
        ttl_multipliers = {
            "concept_explanation": 2.0,    # Stable content, longer cache
            "quiz_generation": 0.5,        # Variable content, shorter cache
            "study_suggestions": 0.25,     # Personalized, very short cache
            "concept_map": 1.5,            # Relatively stable, medium cache
            "general": 1.0                 # Default
        }
        
        ttl = int(base_ttl * ttl_multipliers.get(content_type, 1.0))
        
        # Adjust based on response quality indicators
        if response.tokens_used > 1000:  # Comprehensive response
            ttl = int(ttl * 1.5)
        
        if response.response_time_ms > 10000:  # Slow generation
            ttl = int(ttl * 2.0)
        
        # Ensure reasonable bounds
        return max(300, min(ttl, 86400))  # 5 minutes to 24 hours
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired"""
        age_seconds = (datetime.now() - entry.created_at).total_seconds()
        return age_seconds > entry.ttl_seconds
    
    async def _check_and_enforce_limits(self) -> bool:
        """Check cache limits and evict entries if needed"""
        
        # Check entry count limit
        if len(self.cache) >= self.max_entries:
            await self._evict_entries(count=int(self.max_entries * 0.1))
        
        # Check size limit
        size_mb = self.cache_stats["total_size_bytes"] / (1024 * 1024)
        if size_mb >= self.max_size_mb:
            await self._evict_entries(size_target=int(self.max_size_mb * 0.8 * 1024 * 1024))
        
        return True
    
    async def _evict_entries(self, count: Optional[int] = None, 
                           size_target: Optional[int] = None) -> int:
        """Evict cache entries using LRU strategy"""
        
        if not self.cache:
            return 0
        
        # Sort by access time (oldest first)
        entries_by_age = sorted(
            self.cache.items(),
            key=lambda x: x[1].accessed_at
        )
        
        evicted_count = 0
        current_size = self.cache_stats["total_size_bytes"]
        
        for key, entry in entries_by_age:
            if count and evicted_count >= count:
                break
            if size_target and current_size <= size_target:
                break
            
            await self._remove_entry(key)
            current_size -= entry.size_bytes
            evicted_count += 1
        
        self.cache_stats["evictions"] += evicted_count
        self.logger.info(f"Evicted {evicted_count} cache entries")
        
        return evicted_count
    
    async def _remove_entry(self, key: str) -> bool:
        """Remove single cache entry"""
        
        if key in self.cache:
            entry = self.cache[key]
            del self.cache[key]
            
            self.cache_stats["total_entries"] -= 1
            self.cache_stats["total_size_bytes"] -= entry.size_bytes
            
            return True
        
        return False
    
    async def _maintenance_loop(self):
        """Background maintenance for cache cleanup"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                
                # Remove expired entries
                expired_keys = [
                    key for key, entry in self.cache.items()
                    if self._is_expired(entry)
                ]
                
                for key in expired_keys:
                    await self._remove_entry(key)
                
                if expired_keys:
                    self.logger.debug(f"Removed {len(expired_keys)} expired cache entries")
                
                # Log cache statistics
                self.logger.debug(f"Cache stats: {self.cache_stats}")
                
            except Exception as e:
                self.logger.error(f"Cache maintenance error: {str(e)}")
    
    async def clear(self) -> bool:
        """Clear entire cache"""
        
        try:
            self.cache.clear()
            self.cache_stats = {
                "hits": 0,
                "misses": 0,
                "evictions": 0,
                "total_entries": 0,
                "total_size_bytes": 0
            }
            
            self.logger.info("Cache cleared successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {str(e)}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "enabled": self.settings.enable_caching,
            "total_entries": len(self.cache),
            "max_entries": self.max_entries,
            "size_mb": round(self.cache_stats["total_size_bytes"] / (1024 * 1024), 2),
            "max_size_mb": self.max_size_mb,
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests,
            "hits": self.cache_stats["hits"],
            "misses": self.cache_stats["misses"],
            "evictions": self.cache_stats["evictions"],
            "compression_threshold_bytes": self.compression_threshold,
            "default_ttl_seconds": self.default_ttl
        }
    
    async def get_cache_keys(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get cache keys with metadata for debugging"""
        
        keys_info = []
        
        for key, entry in list(self.cache.items())[:limit]:
            keys_info.append({
                "key": key[:16] + "...",
                "created_at": entry.created_at.isoformat(),
                "accessed_at": entry.accessed_at.isoformat(),
                "access_count": entry.access_count,
                "ttl_seconds": entry.ttl_seconds,
                "size_bytes": entry.size_bytes,
                "compressed": entry.compressed,
                "expired": self._is_expired(entry)
            })
        
        return keys_info
    
    async def export_cache(self, filepath: str) -> bool:
        """Export cache to file for backup"""
        
        try:
            cache_data = {
                "exported_at": datetime.now().isoformat(),
                "stats": self.cache_stats,
                "entries": {}
            }
            
            for key, entry in self.cache.items():
                cache_data["entries"][key] = {
                    "response": asdict(entry.response),
                    "metadata": {
                        "created_at": entry.created_at.isoformat(),
                        "accessed_at": entry.accessed_at.isoformat(),
                        "access_count": entry.access_count,
                        "ttl_seconds": entry.ttl_seconds,
                        "compressed": entry.compressed,
                        "size_bytes": entry.size_bytes
                    }
                }
            
            # Save to file
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            self.logger.info(f"Cache exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export cache: {str(e)}")
            return False
