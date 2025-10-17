"""
Curriculum Package for ScienceGPT v3.0
Complete NCERT curriculum mapping and topic management
"""

from .ncert_curriculum import NCERTCurriculum
from .topic_mapper import TopicMapper
from .learning_paths import LearningPathGenerator

__all__ = ["NCERTCurriculum", "TopicMapper", "LearningPathGenerator"]
