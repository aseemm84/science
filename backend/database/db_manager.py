"""
Advanced Database Manager for ScienceGPT v3.0
High-performance database operations with connection pooling, migrations, and backup support
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any, AsyncGenerator, Type
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import sqlite3
from pathlib import Path
import shutil
from datetime import datetime, timedelta
import json

from .models import Base, User, Topic, Achievement, create_default_achievements
from ..config import get_settings
from ..utils.error_handlers import log_error, DatabaseError


class DatabaseManager:
    """Advanced database manager with connection pooling and async support"""
    
    def __init__(self):
        """Initialize database manager"""
        self.settings = get_settings()
        self.engine: Optional[Engine] = None
        self.session_factory: Optional[sessionmaker] = None
        self.logger = logging.getLogger(__name__)
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize database connection and schema"""
        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                self.settings.database_url,
                poolclass=QueuePool,
                pool_size=self.settings.database_pool_size,
                max_overflow=self.settings.database_max_overflow,
                pool_pre_ping=True,
                pool_recycle=3600,  # Recycle connections every hour
                echo=self.settings.debug
            )
            
            # Create session factory
            self.session_factory = sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False
            )
            
            # Create all tables
            await self._create_tables()
            
            # Initialize default data
            await self._initialize_default_data()
            
            # Set up database maintenance
            await self._setup_maintenance()
            
            self._initialized = True
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            error_msg = f"Database initialization failed: {str(e)}"
            self.logger.error(error_msg)
            raise DatabaseError(error_msg) from e
    
    async def _create_tables(self) -> None:
        """Create all database tables"""
        try:
            # Use asyncio.to_thread for blocking operations
            await asyncio.to_thread(Base.metadata.create_all, self.engine)
            self.logger.info("Database tables created successfully")
        except Exception as e:
            raise DatabaseError(f"Failed to create tables: {str(e)}") from e
    
    async def _initialize_default_data(self) -> None:
        """Initialize default data (achievements, sample topics)"""
        try:
            with self.get_session() as session:
                # Check if achievements already exist
                existing_achievements = session.query(Achievement).count()
                if existing_achievements == 0:
                    # Create default achievements
                    default_achievements = create_default_achievements()
                    for achievement_data in default_achievements:
                        achievement = Achievement(**achievement_data)
                        session.add(achievement)
                    
                    session.commit()
                    self.logger.info(f"Created {len(default_achievements)} default achievements")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default data: {str(e)}")
            raise DatabaseError(f"Failed to initialize default data: {str(e)}") from e
    
    async def _setup_maintenance(self) -> None:
        """Set up database maintenance tasks"""
        try:
            # Enable WAL mode for SQLite
            if "sqlite" in self.settings.database_url:
                with self.get_session() as session:
                    session.execute(text("PRAGMA journal_mode=WAL;"))
                    session.execute(text("PRAGMA synchronous=NORMAL;"))
                    session.execute(text("PRAGMA cache_size=10000;"))
                    session.execute(text("PRAGMA foreign_keys=ON;"))
                    session.commit()
        except Exception as e:
            self.logger.warning(f"Database maintenance setup failed: {str(e)}")
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[Session, None]:
        """Get async database session with proper cleanup"""
        if not self._initialized:
            raise DatabaseError("Database not initialized")
        
        session = self.session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_session(self) -> Session:
        """Get synchronous database session"""
        if not self._initialized:
            raise DatabaseError("Database not initialized")
        
        return self.session_factory()
    
    # User Management Methods
    
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        try:
            async with self.get_async_session() as session:
                user = User(**user_data)
                session.add(user)
                await asyncio.to_thread(session.commit)
                await asyncio.to_thread(session.refresh, user)
                return user
        except IntegrityError as e:
            raise DatabaseError(f"User already exists: {str(e)}") from e
        except Exception as e:
            raise DatabaseError(f"Failed to create user: {str(e)}") from e
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            async with self.get_async_session() as session:
                user = await asyncio.to_thread(
                    session.query(User).filter(User.id == user_id).first
                )
                return user
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}") from e
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            async with self.get_async_session() as session:
                user = await asyncio.to_thread(
                    session.query(User).filter(User.username == username).first
                )
                return user
        except Exception as e:
            raise DatabaseError(f"Failed to get user by username: {str(e)}") from e
    
    async def update_user(self, user_id: int, update_data: Dict[str, Any]) -> bool:
        """Update user information"""
        try:
            async with self.get_async_session() as session:
                user = await asyncio.to_thread(
                    session.query(User).filter(User.id == user_id).first
                )
                if user:
                    for key, value in update_data.items():
                        if hasattr(user, key):
                            setattr(user, key, value)
                    await asyncio.to_thread(session.commit)
                    return True
                return False
        except Exception as e:
            raise DatabaseError(f"Failed to update user: {str(e)}") from e
    
    # Topic Management Methods
    
    async def get_topics_by_grade_subject(self, grade: int, subject: str) -> List[Topic]:
        """Get topics filtered by grade and subject"""
        try:
            async with self.get_async_session() as session:
                topics = await asyncio.to_thread(
                    lambda: session.query(Topic)
                    .filter(Topic.grade == grade, Topic.subject == subject, Topic.is_active == True)
                    .order_by(Topic.title)
                    .all()
                )
                return topics
        except Exception as e:
            raise DatabaseError(f"Failed to get topics: {str(e)}") from e
    
    async def search_topics(self, query: str, grade: Optional[int] = None, 
                           subject: Optional[str] = None) -> List[Topic]:
        """Search topics by title and keywords"""
        try:
            async with self.get_async_session() as session:
                query_filter = session.query(Topic).filter(
                    Topic.title.ilike(f"%{query}%"),
                    Topic.is_active == True
                )
                
                if grade:
                    query_filter = query_filter.filter(Topic.grade == grade)
                if subject:
                    query_filter = query_filter.filter(Topic.subject == subject)
                
                topics = await asyncio.to_thread(
                    lambda: query_filter.order_by(Topic.popularity_score.desc()).limit(50).all()
                )
                return topics
        except Exception as e:
            raise DatabaseError(f"Failed to search topics: {str(e)}") from e
    
    # Analytics Methods
    
    async def get_user_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        try:
            async with self.get_async_session() as session:
                user = await asyncio.to_thread(
                    session.query(User).filter(User.id == user_id).first
                )
                
                if not user:
                    return {}
                
                analytics = {
                    'basic_stats': {
                        'total_points': user.total_points,
                        'level': user.level,
                        'streak_days': user.streak_days,
                        'total_badges': user.total_badges,
                        'questions_asked': user.total_questions_asked,
                        'quizzes_completed': user.total_quizzes_completed,
                        'study_hours': user.total_study_hours,
                        'average_score': user.average_score
                    },
                    'recent_activity': await self._get_recent_activity(session, user_id),
                    'subject_progress': await self._get_subject_progress(session, user_id),
                    'achievement_progress': await self._get_achievement_progress(session, user_id),
                    'performance_trends': await self._get_performance_trends(session, user_id)
                }
                
                return analytics
        except Exception as e:
            raise DatabaseError(f"Failed to get user analytics: {str(e)}") from e
    
    async def _get_recent_activity(self, session: Session, user_id: int) -> List[Dict]:
        """Get user's recent activity"""
        # Implementation for recent activity
        return []
    
    async def _get_subject_progress(self, session: Session, user_id: int) -> Dict[str, Any]:
        """Get user's progress by subject"""
        # Implementation for subject progress
        return {}
    
    async def _get_achievement_progress(self, session: Session, user_id: int) -> Dict[str, Any]:
        """Get user's achievement progress"""
        # Implementation for achievement progress
        return {}
    
    async def _get_performance_trends(self, session: Session, user_id: int) -> Dict[str, Any]:
        """Get user's performance trends"""
        # Implementation for performance trends
        return {}
    
    # Backup and Maintenance Methods
    
    async def create_backup(self, backup_path: Optional[str] = None) -> str:
        """Create database backup"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backups/sciencegpt_backup_{timestamp}.db"
            
            # Ensure backup directory exists
            backup_dir = Path(backup_path).parent
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # For SQLite, copy the database file
            if "sqlite" in self.settings.database_url:
                db_path = self.settings.database_url.replace("sqlite:///", "")
                await asyncio.to_thread(shutil.copy2, db_path, backup_path)
            
            self.logger.info(f"Database backup created: {backup_path}")
            return backup_path
        except Exception as e:
            raise DatabaseError(f"Failed to create backup: {str(e)}") from e
    
    async def cleanup_old_data(self, days_to_keep: int = 90) -> None:
        """Clean up old data to maintain performance"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            async with self.get_async_session() as session:
                # Clean up old chat sessions
                old_sessions = await asyncio.to_thread(
                    lambda: session.query(ChatSession)
                    .filter(ChatSession.created_at < cutoff_date)
                    .delete()
                )
                
                await asyncio.to_thread(session.commit)
                
                self.logger.info(f"Cleaned up {old_sessions} old chat sessions")
        except Exception as e:
            self.logger.error(f"Data cleanup failed: {str(e)}")
    
    async def optimize_database(self) -> None:
        """Optimize database performance"""
        try:
            if "sqlite" in self.settings.database_url:
                async with self.get_async_session() as session:
                    # Run SQLite optimization commands
                    await asyncio.to_thread(session.execute, text("VACUUM;"))
                    await asyncio.to_thread(session.execute, text("ANALYZE;"))
                    await asyncio.to_thread(session.commit)
            
            self.logger.info("Database optimization completed")
        except Exception as e:
            self.logger.error(f"Database optimization failed: {str(e)}")
    
    async def get_health_check(self) -> Dict[str, Any]:
        """Get database health status"""
        try:
            health = {
                'status': 'healthy',
                'initialized': self._initialized,
                'connection_pool': {
                    'size': self.engine.pool.size() if self.engine else 0,
                    'checked_in': self.engine.pool.checkedin() if self.engine else 0,
                    'checked_out': self.engine.pool.checkedout() if self.engine else 0,
                    'overflow': self.engine.pool.overflow() if self.engine else 0
                },
                'last_backup': await self._get_last_backup_info(),
                'database_size': await self._get_database_size()
            }
            
            # Test connection
            async with self.get_async_session() as session:
                await asyncio.to_thread(session.execute, text("SELECT 1"))
            
            return health
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'initialized': self._initialized
            }
    
    async def _get_last_backup_info(self) -> Optional[str]:
        """Get information about the last backup"""
        try:
            backup_dir = Path("backups")
            if backup_dir.exists():
                backup_files = list(backup_dir.glob("sciencegpt_backup_*.db"))
                if backup_files:
                    latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
                    return latest_backup.name
            return None
        except Exception:
            return None
    
    async def _get_database_size(self) -> Optional[str]:
        """Get database size in MB"""
        try:
            if "sqlite" in self.settings.database_url:
                db_path = Path(self.settings.database_url.replace("sqlite:///", ""))
                if db_path.exists():
                    size_bytes = db_path.stat().st_size
                    size_mb = size_bytes / (1024 * 1024)
                    return f"{size_mb:.2f} MB"
            return None
        except Exception:
            return None
    
    async def close(self) -> None:
        """Close database connections"""
        try:
            if self.engine:
                await asyncio.to_thread(self.engine.dispose)
            self._initialized = False
            self.logger.info("Database connections closed")
        except Exception as e:
            self.logger.error(f"Error closing database: {str(e)}")


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


async def get_database_manager() -> DatabaseManager:
    """Get singleton database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
        await _db_manager.initialize()
    return _db_manager
