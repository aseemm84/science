"""
Application Configuration Management
Centralized configuration using Pydantic Settings
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field, validator
from functools import lru_cache


class AppConfig(BaseSettings):
    """Application configuration with environment variable support"""
    
    # Application Settings
    app_name: str = Field(default="ScienceGPT v3.0", env="APP_NAME")
    app_version: str = Field(default="3.0.0", env="APP_VERSION")
    app_env: str = Field(default="development", env="APP_ENV")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///sciencegpt_v3.db", env="DATABASE_URL")
    database_pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    
    # AI/LLM Configuration
    groq_api_key: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Cache Configuration
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    enable_caching: bool = Field(default=True, env="ENABLE_CACHING")
    
    # Security Settings
    secret_key: str = Field(default="dev_secret_key_change_in_production", env="SECRET_KEY")
    encryption_key: Optional[str] = Field(default=None, env="ENCRYPTION_KEY")
    
    # Performance Settings
    max_concurrent_requests: int = Field(default=50, env="MAX_CONCURRENT_REQUESTS")
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")
    rate_limit_per_minute: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/sciencegpt.log", env="LOG_FILE")
    enable_debug_logging: bool = Field(default=False, env="ENABLE_DEBUG_LOGGING")
    
    # Feature Flags
    enable_analytics: bool = Field(default=True, env="ENABLE_ANALYTICS")
    enable_gamification: bool = Field(default=True, env="ENABLE_GAMIFICATION")
    enable_offline_mode: bool = Field(default=False, env="ENABLE_OFFLINE_MODE")
    enable_voice_features: bool = Field(default=False, env="ENABLE_VOICE_FEATURES")
    
    # UI/UX Settings
    default_theme: str = Field(default="light", env="DEFAULT_THEME")
    enable_animations: bool = Field(default=True, env="ENABLE_ANIMATIONS")
    mobile_responsive: bool = Field(default=True, env="MOBILE_RESPONSIVE")
    
    # Curriculum Settings
    default_curriculum: str = Field(default="NCERT", env="DEFAULT_CURRICULUM")
    supported_languages: str = Field(
        default="English,Hindi,Tamil,Telugu,Bengali,Marathi,Gujarati,Kannada,Malayalam,Punjabi",
        env="SUPPORTED_LANGUAGES"
    )
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'log_level must be one of: {valid_levels}')
        return v.upper()
    
    @validator('app_env')
    def validate_app_env(cls, v):
        """Validate application environment"""
        valid_envs = ['development', 'testing', 'production']
        if v.lower() not in valid_envs:
            raise ValueError(f'app_env must be one of: {valid_envs}')
        return v.lower()
    
    @validator('default_theme')
    def validate_theme(cls, v):
        """Validate default theme"""
        valid_themes = ['light', 'dark']
        if v.lower() not in valid_themes:
            raise ValueError(f'default_theme must be one of: {valid_themes}')
        return v.lower()
    
    def get_supported_languages_list(self) -> List[str]:
        """Get supported languages as a list"""
        return [lang.strip() for lang in self.supported_languages.split(',')]
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.app_env == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.app_env == 'development'
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> AppConfig:
    """Get cached application settings"""
    return AppConfig()


# Export settings instance
settings = get_settings()
