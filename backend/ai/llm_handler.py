"""
Advanced LLM Handler for ScienceGPT v3.0
Multi-provider AI integration with intelligent routing, caching, and error handling
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import hashlib
import time

# LLM Provider imports
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .prompt_templates import PromptTemplates
from .response_cache import ResponseCache
from ..config import get_settings
from ..utils.error_handlers import log_error, LLMError
from ..utils.validators import validate_input_text, sanitize_input


class LLMProvider(Enum):
    """Available LLM providers"""
    GROQ = "groq"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: LLMProvider
    model: str
    max_tokens: int
    temperature: float
    timeout: int
    cost_per_token: float
    
    
@dataclass
class LLMResponse:
    """Standardized LLM response"""
    content: str
    provider: LLMProvider
    model: str
    tokens_used: int
    response_time_ms: int
    cached: bool
    timestamp: datetime
    metadata: Dict[str, Any]


class RateLimiter:
    """Advanced rate limiter with per-provider limits"""
    
    def __init__(self):
        self.requests = {}
        self.settings = get_settings()
    
    async def can_make_request(self, provider: LLMProvider) -> Tuple[bool, Optional[str]]:
        """Check if request can be made for given provider"""
        now = time.time()
        provider_key = provider.value
        
        # Initialize if not exists
        if provider_key not in self.requests:
            self.requests[provider_key] = []
        
        # Clean old requests (1 minute window)
        self.requests[provider_key] = [
            req_time for req_time in self.requests[provider_key]
            if now - req_time < 60
        ]
        
        # Check rate limits per provider
        limits = {
            LLMProvider.GROQ: 30,      # 30 per minute
            LLMProvider.OPENAI: 60,    # 60 per minute  
            LLMProvider.ANTHROPIC: 50  # 50 per minute
        }
        
        current_requests = len(self.requests[provider_key])
        limit = limits.get(provider, 30)
        
        if current_requests >= limit:
            wait_time = 60 - (now - min(self.requests[provider_key]))
            return False, f"Rate limit exceeded. Try again in {int(wait_time)} seconds."
        
        return True, None
    
    async def log_request(self, provider: LLMProvider) -> None:
        """Log a request for rate limiting"""
        now = time.time()
        provider_key = provider.value
        
        if provider_key not in self.requests:
            self.requests[provider_key] = []
        
        self.requests[provider_key].append(now)


class LLMHandler:
    """Advanced LLM handler with multi-provider support and intelligent routing"""
    
    def __init__(self):
        """Initialize LLM handler"""
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        self.prompt_templates = PromptTemplates()
        self.response_cache = ResponseCache()
        self.rate_limiter = RateLimiter()
        
        # Initialize providers
        self.providers = {}
        self._initialize_providers()
        
        # Provider configurations
        self.provider_configs = {
            LLMProvider.GROQ: LLMConfig(
                provider=LLMProvider.GROQ,
                model="llama3-8b-8192",
                max_tokens=1500,
                temperature=0.7,
                timeout=30,
                cost_per_token=0.0001
            ),
            LLMProvider.OPENAI: LLMConfig(
                provider=LLMProvider.OPENAI,
                model="gpt-3.5-turbo",
                max_tokens=1500,
                temperature=0.7,
                timeout=30,
                cost_per_token=0.0015
            ),
            LLMProvider.ANTHROPIC: LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                model="claude-3-haiku-20240307",
                max_tokens=1500,
                temperature=0.7,
                timeout=30,
                cost_per_token=0.0008
            )
        }
        
    def _initialize_providers(self) -> None:
        """Initialize available LLM providers"""
        # Initialize Groq
        if GROQ_AVAILABLE and self.settings.groq_api_key:
            try:
                self.providers[LLMProvider.GROQ] = Groq(api_key=self.settings.groq_api_key)
                self.logger.info("Groq provider initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Groq: {str(e)}")
        
        # Initialize OpenAI
        if OPENAI_AVAILABLE and self.settings.openai_api_key:
            try:
                openai.api_key = self.settings.openai_api_key
                self.providers[LLMProvider.OPENAI] = openai
                self.logger.info("OpenAI provider initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize OpenAI: {str(e)}")
        
        # Initialize Anthropic
        if ANTHROPIC_AVAILABLE and self.settings.anthropic_api_key:
            try:
                self.providers[LLMProvider.ANTHROPIC] = anthropic.Anthropic(
                    api_key=self.settings.anthropic_api_key
                )
                self.logger.info("Anthropic provider initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Anthropic: {str(e)}")
        
        if not self.providers:
            raise LLMError("No LLM providers available. Please configure API keys.")
    
    def _select_provider(self, request_type: str = "general") -> LLMProvider:
        """Intelligently select the best provider for the request"""
        available_providers = list(self.providers.keys())
        
        if not available_providers:
            raise LLMError("No LLM providers available")
        
        # Provider selection logic based on request type
        preference_order = {
            "general": [LLMProvider.GROQ, LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
            "complex": [LLMProvider.OPENAI, LLMProvider.ANTHROPIC, LLMProvider.GROQ],
            "creative": [LLMProvider.ANTHROPIC, LLMProvider.OPENAI, LLMProvider.GROQ],
            "factual": [LLMProvider.GROQ, LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
        }
        
        preferred = preference_order.get(request_type, preference_order["general"])
        
        # Return first available provider from preference order
        for provider in preferred:
            if provider in available_providers:
                return provider
        
        return available_providers[0]
    
    async def generate_response(
        self,
        question: str,
        context: Dict[str, Any],
        request_type: str = "general",
        use_cache: bool = True
    ) -> LLMResponse:
        """Generate AI response with multi-provider fallback"""
        
        # Validate and sanitize input
        question = sanitize_input(question)
        if not validate_input_text(question):
            raise LLMError("Invalid input question")
        
        # Check cache first
        if use_cache:
            cached_response = await self.response_cache.get(question, context)
            if cached_response:
                return cached_response
        
        # Select provider
        provider = self._select_provider(request_type)
        
        # Try primary provider, fallback to others if needed
        for attempt_provider in [provider] + [p for p in self.providers.keys() if p != provider]:
            try:
                response = await self._make_request(attempt_provider, question, context)
                
                # Cache successful response
                if use_cache:
                    await self.response_cache.set(question, context, response)
                
                return response
                
            except Exception as e:
                self.logger.warning(f"Provider {attempt_provider.value} failed: {str(e)}")
                continue
        
        raise LLMError("All LLM providers failed")
    
    async def _make_request(
        self,
        provider: LLMProvider,
        question: str,
        context: Dict[str, Any]
    ) -> LLMResponse:
        """Make request to specific provider"""
        
        # Check rate limits
        can_request, error_msg = await self.rate_limiter.can_make_request(provider)
        if not can_request:
            raise LLMError(f"Rate limit exceeded: {error_msg}")
        
        # Log request
        await self.rate_limiter.log_request(provider)
        
        # Get provider config
        config = self.provider_configs[provider]
        
        # Build prompt
        system_prompt = self.prompt_templates.build_system_prompt(context)
        user_prompt = self.prompt_templates.build_user_prompt(question, context)
        
        start_time = time.time()
        
        try:
            if provider == LLMProvider.GROQ:
                response = await self._make_groq_request(config, system_prompt, user_prompt)
            elif provider == LLMProvider.OPENAI:
                response = await self._make_openai_request(config, system_prompt, user_prompt)
            elif provider == LLMProvider.ANTHROPIC:
                response = await self._make_anthropic_request(config, system_prompt, user_prompt)
            else:
                raise LLMError(f"Unsupported provider: {provider}")
            
            response_time = int((time.time() - start_time) * 1000)
            
            return LLMResponse(
                content=response["content"],
                provider=provider,
                model=config.model,
                tokens_used=response.get("tokens_used", 0),
                response_time_ms=response_time,
                cached=False,
                timestamp=datetime.now(),
                metadata=response.get("metadata", {})
            )
            
        except Exception as e:
            raise LLMError(f"Provider {provider.value} request failed: {str(e)}") from e
    
    async def _make_groq_request(
        self,
        config: LLMConfig,
        system_prompt: str,
        user_prompt: str
    ) -> Dict[str, Any]:
        """Make request to Groq"""
        client = self.providers[LLMProvider.GROQ]
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            timeout=config.timeout
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
            "metadata": {
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }
        }
    
    async def _make_openai_request(
        self,
        config: LLMConfig,
        system_prompt: str,
        user_prompt: str
    ) -> Dict[str, Any]:
        """Make request to OpenAI"""
        client = self.providers[LLMProvider.OPENAI]
        
        response = await asyncio.to_thread(
            client.ChatCompletion.create,
            model=config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            timeout=config.timeout
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "metadata": {
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }
        }
    
    async def _make_anthropic_request(
        self,
        config: LLMConfig,
        system_prompt: str,
        user_prompt: str
    ) -> Dict[str, Any]:
        """Make request to Anthropic"""
        client = self.providers[LLMProvider.ANTHROPIC]
        
        response = await asyncio.to_thread(
            client.messages.create,
            model=config.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            timeout=config.timeout
        )
        
        return {
            "content": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "metadata": {
                "model": response.model,
                "stop_reason": response.stop_reason
            }
        }
    
    # Specialized Methods for Different Use Cases
    
    async def explain_concept(
        self,
        topic: str,
        grade: int,
        subject: str,
        language: str = "English",
        include_examples: bool = True
    ) -> LLMResponse:
        """Generate concept explanation"""
        context = {
            "type": "concept_explanation",
            "topic": topic,
            "grade": grade,
            "subject": subject,
            "language": language,
            "include_examples": include_examples,
            "curriculum": "NCERT"
        }
        
        return await self.generate_response(
            question=f"Explain the concept of {topic}",
            context=context,
            request_type="factual"
        )
    
    async def generate_quiz_question(
        self,
        topic: str,
        grade: int,
        subject: str,
        difficulty: str = "intermediate"
    ) -> LLMResponse:
        """Generate quiz questions"""
        context = {
            "type": "quiz_generation",
            "topic": topic,
            "grade": grade,
            "subject": subject,
            "difficulty": difficulty,
            "question_type": "multiple_choice",
            "num_options": 4
        }
        
        return await self.generate_response(
            question=f"Generate a {difficulty} quiz question about {topic}",
            context=context,
            request_type="creative"
        )
    
    async def provide_study_suggestions(
        self,
        student_data: Dict[str, Any]
    ) -> LLMResponse:
        """Generate personalized study suggestions"""
        context = {
            "type": "study_suggestions",
            "student_grade": student_data.get("grade", 6),
            "weak_subjects": student_data.get("weak_subjects", []),
            "strong_subjects": student_data.get("strong_subjects", []),
            "recent_topics": student_data.get("recent_topics", []),
            "learning_goals": student_data.get("learning_goals", [])
        }
        
        return await self.generate_response(
            question="Provide personalized study suggestions",
            context=context,
            request_type="general"
        )
    
    async def create_concept_map(
        self,
        topic: str,
        grade: int,
        subject: str
    ) -> LLMResponse:
        """Generate concept map structure"""
        context = {
            "type": "concept_map",
            "topic": topic,
            "grade": grade,
            "subject": subject,
            "format": "hierarchical",
            "max_nodes": 15
        }
        
        return await self.generate_response(
            question=f"Create a concept map for {topic}",
            context=context,
            request_type="creative"
        )
    
    # Utility Methods
    
    async def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {}
        
        for provider in LLMProvider:
            status[provider.value] = {
                "available": provider in self.providers,
                "config": self.provider_configs[provider].__dict__ if provider in self.provider_configs else None,
                "recent_requests": len(self.rate_limiter.requests.get(provider.value, [])),
                "rate_limit": await self.rate_limiter.can_make_request(provider)
            }
        
        return status
    
    async def clear_cache(self) -> bool:
        """Clear response cache"""
        try:
            await self.response_cache.clear()
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {str(e)}")
            return False
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_requests": sum(len(requests) for requests in self.rate_limiter.requests.values()),
            "cache_stats": await self.response_cache.get_stats(),
            "provider_distribution": {
                provider.value: len(self.rate_limiter.requests.get(provider.value, []))
                for provider in LLMProvider
            }
        }
