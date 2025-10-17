"""
Database Package for ScienceGPT v3.0
Advanced database management with SQLAlchemy
"""

from .db_manager import DatabaseManager
from .models import *

__all__ = ["DatabaseManager"]
