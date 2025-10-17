"""
Topic Mapper for ScienceGPT v3.0
Maps topics to difficulty levels, learning paths, and related concepts
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from .ncert_curriculum import NCERTCurriculum, Topic, Subject, Difficulty


@dataclass
class TopicRelationship:
    """Relationship between topics"""
    source_topic_id: str
    target_topic_id: str
    relationship_type: str  # prerequisite, related, builds_upon, applies_to
    strength: float  # 0.0 to 1.0


@dataclass 
class LearningPath:
    """Sequence of topics for learning"""
    path_id: str
    name: str
    description: str
    subject: Subject
    grade_range: Tuple[int, int]
    topics: List[str]  # Topic IDs in sequence
    estimated_hours: int


class TopicMapper:
    """Maps relationships between curriculum topics"""
    
    def __init__(self, curriculum: NCERTCurriculum):
        """Initialize topic mapper"""
        self.curriculum = curriculum
        self.relationships: Dict[str, List[TopicRelationship]] = {}
        self.difficulty_progressions: Dict[str, List[str]] = {}
        self.cross_subject_connections: List[TopicRelationship] = []
        
        self._build_relationships()
        self._identify_progressions()
        self._find_cross_subject_connections()
    
    def _build_relationships(self) -> None:
        """Build relationships between topics"""
        
        # Physics relationships
        self._build_physics_relationships()
        
        # Chemistry relationships  
        self._build_chemistry_relationships()
        
        # Biology relationships
        self._build_biology_relationships()
    
    def _build_physics_relationships(self) -> None:
        """Build physics topic relationships"""
        
        physics_progressions = {
            "motion_and_mechanics": [
                "cl6_sci_motion_types",
                "cl6_sci_measurement", 
                "cl9_sci_motion_velocity",
                "cl9_sci_laws_of_motion",
                "cl11_phy_kinematics",
                "cl11_phy_dynamics",
                "cl12_phy_gravitation"
            ],
            "electricity_and_magnetism": [
                "cl8_sci_static_electricity",
                "cl10_sci_electric_current",
                "cl10_sci_electric_power",
                "cl12_phy_electric_charges",
                "cl12_phy_electric_fields",
                "cl12_phy_magnetic_fields",
                "cl12_phy_electromagnetic_induction"
            ],
            "light_and_optics": [
                "cl6_sci_light_shadow",
                "cl8_sci_light_reflection",
                "cl10_sci_light_reflection",
                "cl10_sci_light_refraction",
                "cl12_phy_ray_optics",
                "cl12_phy_wave_nature_light",
                "cl12_phy_interference"
            ]
        }
        
        for progression_name, topic_ids in physics_progressions.items():
            self.difficulty_progressions[progression_name] = topic_ids
            
            # Create prerequisite relationships
            for i in range(1, len(topic_ids)):
                relationship = TopicRelationship(
                    source_topic_id=topic_ids[i-1],
                    target_topic_id=topic_ids[i],
                    relationship_type="prerequisite",
                    strength=0.8
                )
                
                if topic_ids[i] not in self.relationships:
                    self.relationships[topic_ids[i]] = []
                self.relationships[topic_ids[i]].append(relationship)
    
    def _build_chemistry_relationships(self) -> None:
        """Build chemistry topic relationships"""
        
        chemistry_progressions = {
            "atomic_structure": [
                "cl6_sci_material_properties",
                "cl8_sci_metals_nonmetals",
                "cl9_sci_atoms_molecules",
                "cl9_sci_atomic_structure", 
                "cl11_chem_atomic_structure",
                "cl11_chem_periodic_table",
                "cl12_chem_chemical_bonding"
            ],
            "chemical_reactions": [
                "cl7_sci_physical_chemical_changes",
                "cl8_sci_combustion",
                "cl10_sci_chemical_reactions",
                "cl10_sci_chemical_equations",
                "cl11_chem_thermodynamics",
                "cl12_chem_chemical_kinetics"
            ]
        }
        
        for progression_name, topic_ids in chemistry_progressions.items():
            self.difficulty_progressions[progression_name] = topic_ids
    
    def _build_biology_relationships(self) -> None:
        """Build biology topic relationships"""
        
        biology_progressions = {
            "cell_biology": [
                "cl6_sci_basic_life_processes",
                "cl8_sci_cell_structure",
                "cl9_sci_fundamental_unit_life",
                "cl11_bio_cell_structure_function",
                "cl11_bio_biomolecules",
                "cl12_bio_molecular_inheritance"
            ],
            "human_physiology": [
                "cl6_sci_body_movements",
                "cl7_sci_nutrition_animals",
                "cl10_sci_nutrition",
                "cl10_sci_respiration",
                "cl11_bio_transport_plants",
                "cl11_bio_human_physiology",
                "cl12_bio_reproduction_organisms"
            ]
        }
        
        for progression_name, topic_ids in biology_progressions.items():
            self.difficulty_progressions[progression_name] = topic_ids
    
    def _identify_progressions(self) -> None:
        """Identify difficulty progressions within subjects"""
        # Already handled in individual subject relationship builders
        pass
    
    def _find_cross_subject_connections(self) -> None:
        """Find connections between different subjects"""
        
        cross_connections = [
            # Physics-Chemistry connections
            ("cl12_phy_atomic_structure", "cl12_chem_atomic_structure", "related", 0.9),
            ("cl10_sci_electric_current", "cl10_sci_chemical_effects_current", "applies_to", 0.7),
            ("cl11_phy_thermodynamics", "cl11_chem_thermodynamics", "related", 0.8),
            
            # Biology-Chemistry connections  
            ("cl10_sci_nutrition", "cl11_chem_organic_chemistry", "applies_to", 0.6),
            ("cl12_bio_molecular_inheritance", "cl12_chem_biomolecules", "builds_upon", 0.8),
            ("cl11_bio_photosynthesis", "cl11_chem_chemical_energetics", "applies_to", 0.7),
            
            # Physics-Biology connections
            ("cl10_sci_light_reflection", "cl11_bio_human_eye", "applies_to", 0.6),
            ("cl12_phy_electromagnetic_radiation", "cl11_bio_photosynthesis", "enables", 0.7),
        ]
        
        for source, target, rel_type, strength in cross_connections:
            relationship = TopicRelationship(
                source_topic_id=source,
                target_topic_id=target, 
                relationship_type=rel_type,
                strength=strength
            )
            self.cross_subject_connections.append(relationship)
    
    def get_related_topics(self, topic_id: str, max_results: int = 10) -> List[Tuple[Topic, str, float]]:
        """Get topics related to the given topic"""
        
        related = []
        
        # Get direct relationships
        if topic_id in self.relationships:
            for rel in self.relationships[topic_id]:
                related_topic = self.curriculum.get_topic_by_id(rel.target_topic_id)
                if related_topic:
                    related.append((related_topic, rel.relationship_type, rel.strength))
        
        # Get reverse relationships
        for other_topic_id, relationships in self.relationships.items():
            for rel in relationships:
                if rel.target_topic_id == topic_id:
                    related_topic = self.curriculum.get_topic_by_id(rel.source_topic_id)
                    if related_topic:
                        related.append((related_topic, f"reverse_{rel.relationship_type}", rel.strength))
        
        # Sort by strength and return top results
        related.sort(key=lambda x: x[2], reverse=True)
        return related[:max_results]
    
    def get_learning_path(self, topic_id: str) -> Optional[List[Topic]]:
        """Get optimal learning path to reach a topic"""
        
        # Find which progression this topic belongs to
        for progression_name, topic_ids in self.difficulty_progressions.items():
            if topic_id in topic_ids:
                target_index = topic_ids.index(topic_id)
                
                # Return all topics up to and including the target
                path_topics = []
                for i in range(target_index + 1):
                    topic = self.curriculum.get_topic_by_id(topic_ids[i])
                    if topic:
                        path_topics.append(topic)
                
                return path_topics
        
        return None
    
    def suggest_next_topics(self, completed_topic_ids: List[str], subject: Optional[Subject] = None) -> List[Topic]:
        """Suggest next topics based on completed topics"""
        
        suggestions = []
        completed_set = set(completed_topic_ids)
        
        # Look through progressions to find next logical topics
        for progression_name, topic_ids in self.difficulty_progressions.items():
            
            # Check if any topic in this progression has been completed
            completed_in_progression = [tid for tid in topic_ids if tid in completed_set]
            
            if completed_in_progression:
                # Find the highest completed topic
                max_completed_index = max(topic_ids.index(tid) for tid in completed_in_progression)
                
                # Suggest the next topic if it exists
                if max_completed_index + 1 < len(topic_ids):
                    next_topic_id = topic_ids[max_completed_index + 1]
                    next_topic = self.curriculum.get_topic_by_id(next_topic_id)
                    
                    if next_topic and (not subject or next_topic.subject == subject):
                        suggestions.append(next_topic)
        
        # Remove duplicates and limit results
        seen_topics = set()
        unique_suggestions = []
        
        for topic in suggestions:
            if topic.id not in seen_topics:
                seen_topics.add(topic.id)
                unique_suggestions.append(topic)
        
        return unique_suggestions[:10]
    
    def get_topic_difficulty_score(self, topic_id: str) -> float:
        """Calculate difficulty score for a topic (0.0 to 1.0)"""
        
        topic = self.curriculum.get_topic_by_id(topic_id)
        if not topic:
            return 0.0
        
        base_score = {
            Difficulty.BEGINNER: 0.2,
            Difficulty.INTERMEDIATE: 0.5, 
            Difficulty.ADVANCED: 0.8
        }.get(topic.difficulty, 0.5)
        
        # Adjust based on grade level
        grade_factor = (topic.grade - 1) / 11  # Normalize grade 1-12 to 0-1
        
        # Adjust based on prerequisites
        prereq_count = len(topic.prerequisites)
        prereq_factor = min(prereq_count * 0.1, 0.3)  # Max 0.3 adjustment
        
        final_score = min(1.0, base_score + grade_factor * 0.3 + prereq_factor)
        return final_score
    
    def find_knowledge_gaps(self, completed_topic_ids: List[str], target_topic_id: str) -> List[Topic]:
        """Find knowledge gaps between completed topics and target topic"""
        
        # Get learning path to target
        learning_path = self.get_learning_path(target_topic_id)
        if not learning_path:
            return []
        
        # Find missing topics in the path
        completed_set = set(completed_topic_ids)
        gaps = []
        
        for topic in learning_path:
            if topic.id not in completed_set:
                # Check if this topic's prerequisites are met
                prereqs_met = all(prereq_id in completed_set for prereq_id in topic.prerequisites)
                
                if prereqs_met or not topic.prerequisites:
                    gaps.append(topic)
        
        return gaps
    
    def export_topic_relationships(self) -> Dict[str, Any]:
        """Export topic relationships for visualization or analysis"""
        
        export_data = {
            "progressions": self.difficulty_progressions,
            "relationships": {},
            "cross_subject_connections": []
        }
        
        # Export relationships
        for topic_id, relationships in self.relationships.items():
            export_data["relationships"][topic_id] = [
                {
                    "target": rel.target_topic_id,
                    "type": rel.relationship_type,
                    "strength": rel.strength
                }
                for rel in relationships
            ]
        
        # Export cross-subject connections
        for rel in self.cross_subject_connections:
            export_data["cross_subject_connections"].append({
                "source": rel.source_topic_id,
                "target": rel.target_topic_id,
                "type": rel.relationship_type,
                "strength": rel.strength
            })
        
        return export_data
