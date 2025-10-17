"""
SQLAlchemy Data Models for ScienceGPT v3.0
Comprehensive database schema for all application data
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    ForeignKey, JSON, Float, Enum, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any
import enum


Base = declarative_base()


class UserRole(enum.Enum):
    """User role enumeration"""
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMIN = "admin"


class DifficultyLevel(enum.Enum):
    """Content difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class SubjectType(enum.Enum):
    """Science subjects"""
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"


class User(Base):
    """User model with comprehensive profile data"""
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic Information
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)  # For future authentication
    
    # Profile Information
    full_name = Column(String(100), nullable=True)
    grade = Column(Integer, nullable=False, default=6)
    age = Column(Integer, nullable=True)
    school = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    
    # User Preferences
    preferred_language = Column(String(20), nullable=False, default="English")
    preferred_subject = Column(Enum(SubjectType), nullable=False, default=SubjectType.PHYSICS)
    theme = Column(String(20), nullable=False, default="light")
    timezone = Column(String(50), nullable=False, default="Asia/Kolkata")
    
    # User Role & Status
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    
    # Gamification Data
    total_points = Column(Integer, nullable=False, default=0)
    level = Column(String(20), nullable=False, default="Beginner")
    streak_days = Column(Integer, nullable=False, default=0)
    total_badges = Column(Integer, nullable=False, default=0)
    
    # Analytics
    total_questions_asked = Column(Integer, nullable=False, default=0)
    total_quizzes_completed = Column(Integer, nullable=False, default=0)
    total_study_hours = Column(Float, nullable=False, default=0.0)
    average_score = Column(Float, nullable=False, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_active = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Settings JSON
    preferences = Column(JSON, nullable=True)
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_grade', 'grade'),
        Index('idx_user_active', 'is_active'),
        Index('idx_user_role', 'role'),
    )
    
    @validates('grade')
    def validate_grade(self, key, grade):
        """Validate grade is between 1-12"""
        if grade < 1 or grade > 12:
            raise ValueError("Grade must be between 1 and 12")
        return grade
    
    @validates('email')
    def validate_email(self, key, email):
        """Basic email validation"""
        if email and '@' not in email:
            raise ValueError("Invalid email format")
        return email
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', grade={self.grade})>"


class UserSession(Base):
    """User session tracking for analytics"""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), nullable=False, unique=True)
    
    # Session Data
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_info = Column(JSON, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Session Stats
    questions_asked = Column(Integer, nullable=False, default=0)
    quizzes_completed = Column(Integer, nullable=False, default=0)
    time_spent_minutes = Column(Float, nullable=False, default=0.0)
    
    # Relationship
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, session_id='{self.session_id}')>"


class Topic(Base):
    """NCERT curriculum topics"""
    
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Topic Information
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(Enum(SubjectType), nullable=False)
    grade = Column(Integer, nullable=False)
    chapter = Column(String(100), nullable=True)
    
    # Content
    keywords = Column(JSON, nullable=True)  # List of keywords
    learning_objectives = Column(JSON, nullable=True)  # List of objectives
    prerequisites = Column(JSON, nullable=True)  # List of prerequisite topic IDs
    
    # Difficulty and Metadata
    difficulty = Column(Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.BEGINNER)
    estimated_time_minutes = Column(Integer, nullable=False, default=30)
    popularity_score = Column(Float, nullable=False, default=0.0)
    
    # NCERT Mapping
    ncert_chapter = Column(String(10), nullable=True)  # Like "Ch-1"
    ncert_section = Column(String(50), nullable=True)
    ncert_page_reference = Column(String(20), nullable=True)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    progress_records = relationship("UserProgress", back_populates="topic", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="topic", cascade="all, delete-orphan")
    quiz_questions = relationship("QuizQuestion", back_populates="topic", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_topic_subject_grade', 'subject', 'grade'),
        Index('idx_topic_difficulty', 'difficulty'),
        Index('idx_topic_active', 'is_active'),
        UniqueConstraint('title', 'subject', 'grade', name='uq_topic_title_subject_grade'),
    )
    
    def __repr__(self):
        return f"<Topic(id={self.id}, title='{self.title}', subject={self.subject}, grade={self.grade})>"


class UserProgress(Base):
    """User progress tracking for each topic"""
    
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    
    # Progress Data
    mastery_level = Column(Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.BEGINNER)
    completion_percentage = Column(Float, nullable=False, default=0.0)
    time_spent_minutes = Column(Float, nullable=False, default=0.0)
    
    # Learning Stats
    questions_asked = Column(Integer, nullable=False, default=0)
    correct_answers = Column(Integer, nullable=False, default=0)
    quiz_scores = Column(JSON, nullable=True)  # List of quiz scores
    practice_sessions = Column(Integer, nullable=False, default=0)
    
    # Engagement
    bookmarked = Column(Boolean, nullable=False, default=False)
    last_studied = Column(DateTime(timezone=True), nullable=True)
    study_streak = Column(Integer, nullable=False, default=0)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    topic = relationship("Topic", back_populates="progress_records")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'topic_id', name='uq_user_topic_progress'),
        Index('idx_progress_user_mastery', 'user_id', 'mastery_level'),
        Index('idx_progress_completion', 'completion_percentage'),
    )
    
    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, topic_id={self.topic_id}, mastery={self.mastery_level})>"


class Achievement(Base):
    """Achievement definitions"""
    
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Achievement Info
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=False)  # Emoji or icon name
    category = Column(String(50), nullable=False)  # learning, streak, quiz, etc.
    
    # Requirements
    requirement_type = Column(String(50), nullable=False)  # points, streak, quiz_score, etc.
    requirement_value = Column(Integer, nullable=False)
    requirement_description = Column(Text, nullable=True)
    
    # Rewards
    points_reward = Column(Integer, nullable=False, default=0)
    badge_tier = Column(String(20), nullable=False, default="bronze")  # bronze, silver, gold, platinum
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    is_hidden = Column(Boolean, nullable=False, default=False)  # Secret achievements
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}', category='{self.category}')>"


class UserAchievement(Base):
    """User achievement records"""
    
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    
    # Achievement Data
    earned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    progress_value = Column(Integer, nullable=True)  # Progress when earned
    
    # Metadata
    is_featured = Column(Boolean, nullable=False, default=False)  # Show on profile
    notification_sent = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'achievement_id', name='uq_user_achievement'),
        Index('idx_achievement_earned_at', 'earned_at'),
    )
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class Bookmark(Base):
    """User bookmarks for important content"""
    
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    
    # Content
    title = Column(String(200), nullable=False)
    content_type = Column(String(50), nullable=False)  # question, explanation, quiz, etc.
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    
    # Metadata
    tags = Column(JSON, nullable=True)  # List of user tags
    notes = Column(Text, nullable=True)  # User's personal notes
    
    # Organization
    folder = Column(String(100), nullable=True, default="General")
    is_favorite = Column(Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    topic = relationship("Topic", back_populates="bookmarks")
    
    # Indexes
    __table_args__ = (
        Index('idx_bookmark_user_created', 'user_id', 'created_at'),
        Index('idx_bookmark_folder', 'folder'),
        Index('idx_bookmark_favorite', 'is_favorite'),
    )
    
    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, title='{self.title}')>"


class Quiz(Base):
    """Quiz definitions"""
    
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Quiz Information
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(Enum(SubjectType), nullable=False)
    grade = Column(Integer, nullable=False)
    
    # Quiz Settings
    difficulty = Column(Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.INTERMEDIATE)
    time_limit_minutes = Column(Integer, nullable=True)  # NULL = no time limit
    max_attempts = Column(Integer, nullable=False, default=3)
    passing_score = Column(Integer, nullable=False, default=70)  # Percentage
    
    # Content
    instructions = Column(Text, nullable=True)
    total_questions = Column(Integer, nullable=False, default=0)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    is_featured = Column(Boolean, nullable=False, default=False)
    
    # Analytics
    total_attempts = Column(Integer, nullable=False, default=0)
    average_score = Column(Float, nullable=False, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', subject={self.subject}, grade={self.grade})>"


class QuizQuestion(Base):
    """Individual quiz questions"""
    
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    
    # Question Content
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False, default="multiple_choice")  # multiple_choice, true_false, fill_blank
    
    # Answer Options (JSON format)
    options = Column(JSON, nullable=True)  # For multiple choice: ["A) Option 1", "B) Option 2", ...]
    correct_answer = Column(String(500), nullable=False)
    explanation = Column(Text, nullable=True)
    
    # Question Settings
    points = Column(Integer, nullable=False, default=1)
    difficulty = Column(Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.INTERMEDIATE)
    order_index = Column(Integer, nullable=False, default=0)
    
    # Analytics
    times_asked = Column(Integer, nullable=False, default=0)
    correct_attempts = Column(Integer, nullable=False, default=0)
    average_time_seconds = Column(Float, nullable=False, default=0.0)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    topic = relationship("Topic", back_populates="quiz_questions")
    
    def __repr__(self):
        return f"<QuizQuestion(id={self.id}, quiz_id={self.quiz_id}, question_type='{self.question_type}')>"


class QuizAttempt(Base):
    """User quiz attempts and scores"""
    
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    # Attempt Data
    attempt_number = Column(Integer, nullable=False, default=1)
    score = Column(Integer, nullable=False)  # Percentage score
    points_earned = Column(Integer, nullable=False, default=0)
    
    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    
    # Results
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=True)  # User's answers for each question
    
    # Status
    is_completed = Column(Boolean, nullable=False, default=False)
    passed = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    
    # Indexes
    __table_args__ = (
        Index('idx_attempt_user_quiz', 'user_id', 'quiz_id'),
        Index('idx_attempt_score', 'score'),
        Index('idx_attempt_completed', 'is_completed'),
    )
    
    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, user_id={self.user_id}, quiz_id={self.quiz_id}, score={self.score})>"


class ChatSession(Base):
    """AI chat sessions for learning interactions"""
    
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), nullable=False)
    
    # Session Data
    subject = Column(Enum(SubjectType), nullable=False)
    grade = Column(Integer, nullable=False)
    language = Column(String(20), nullable=False, default="English")
    
    # Content
    question = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)  # Additional context data
    
    # Metadata
    response_time_ms = Column(Integer, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(50), nullable=True)
    
    # User Feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    user_feedback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_chat_user_created', 'user_id', 'created_at'),
        Index('idx_chat_subject_grade', 'subject', 'grade'),
        Index('idx_chat_session', 'session_id'),
    )
    
    def __repr__(self):
        return f"<ChatSession(id={self.id}, user_id={self.user_id}, subject={self.subject})>"


# Additional utility functions for the models

def create_default_achievements():
    """Create default achievements for the system"""
    default_achievements = [
        {
            "name": "First Steps",
            "description": "Asked your first question",
            "icon": "🌱",
            "category": "learning",
            "requirement_type": "questions_asked",
            "requirement_value": 1,
            "points_reward": 10,
            "badge_tier": "bronze"
        },
        {
            "name": "Curious Mind",
            "description": "Asked 10 questions",
            "icon": "🤔", 
            "category": "learning",
            "requirement_type": "questions_asked",
            "requirement_value": 10,
            "points_reward": 25,
            "badge_tier": "bronze"
        },
        {
            "name": "Knowledge Seeker",
            "description": "Asked 50 questions",
            "icon": "📚",
            "category": "learning", 
            "requirement_type": "questions_asked",
            "requirement_value": 50,
            "points_reward": 100,
            "badge_tier": "silver"
        },
        {
            "name": "Quiz Master",
            "description": "Completed 5 quizzes",
            "icon": "🎯",
            "category": "quiz",
            "requirement_type": "quizzes_completed",
            "requirement_value": 5,
            "points_reward": 50,
            "badge_tier": "silver"
        },
        {
            "name": "Perfect Score",
            "description": "Got 100% on a quiz",
            "icon": "🏆",
            "category": "quiz", 
            "requirement_type": "perfect_quiz",
            "requirement_value": 1,
            "points_reward": 100,
            "badge_tier": "gold"
        },
        {
            "name": "Study Streak",
            "description": "Maintained 7-day study streak",
            "icon": "🔥",
            "category": "streak",
            "requirement_type": "streak_days", 
            "requirement_value": 7,
            "points_reward": 75,
            "badge_tier": "gold"
        },
        {
            "name": "Century Club",
            "description": "Earned 100 points",
            "icon": "💯",
            "category": "points",
            "requirement_type": "total_points",
            "requirement_value": 100,
            "points_reward": 0,
            "badge_tier": "silver"
        },
        {
            "name": "Physics Expert",
            "description": "Mastered 20 Physics topics",
            "icon": "⚛️",
            "category": "mastery",
            "requirement_type": "physics_topics_mastered",
            "requirement_value": 20,
            "points_reward": 150,
            "badge_tier": "gold"
        },
        {
            "name": "Chemistry Wizard",
            "description": "Mastered 20 Chemistry topics", 
            "icon": "🧪",
            "category": "mastery",
            "requirement_type": "chemistry_topics_mastered",
            "requirement_value": 20,
            "points_reward": 150,
            "badge_tier": "gold"
        },
        {
            "name": "Biology Explorer",
            "description": "Mastered 20 Biology topics",
            "icon": "🔬", 
            "category": "mastery",
            "requirement_type": "biology_topics_mastered",
            "requirement_value": 20,
            "points_reward": 150,
            "badge_tier": "gold"
        },
        {
            "name": "Science Champion", 
            "description": "Reached Expert level in all subjects",
            "icon": "🏅",
            "category": "mastery",
            "requirement_type": "expert_all_subjects",
            "requirement_value": 1,
            "points_reward": 500,
            "badge_tier": "platinum"
        }
    ]
    
    return default_achievements
