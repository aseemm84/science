"""
ScienceGPT v3.0 Backend Package
Core backend functionality for the ScienceGPT platform
"""

__version__ = "3.0.0"
__author__ = "Aseem Mehrotra"

from .config import AppConfig, get_settings
from .database.db_manager import DatabaseManager
from .ai.llm_handler import LLMHandler
from .curriculum.ncert_curriculum import NCERTCurriculum

__all__ = [
    "AppConfig",
    "get_settings", 
    "DatabaseManager",
    "LLMHandler",
    "NCERTCurriculum"
]
