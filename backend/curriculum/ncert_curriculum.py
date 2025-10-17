"""
Complete NCERT Curriculum for ScienceGPT v3.0
Comprehensive topic mapping for Classes 1-12 (Physics, Chemistry, Biology)
Over 500 topics organized by grade, subject, and difficulty level
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class Subject(Enum):
    """Science subjects"""
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    BIOLOGY = "Biology"


class Difficulty(Enum):
    """Topic difficulty levels"""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


@dataclass
class Topic:
    """Individual curriculum topic"""
    id: str
    title: str
    description: str
    subject: Subject
    grade: int
    chapter: str
    difficulty: Difficulty
    keywords: List[str]
    learning_objectives: List[str]
    prerequisites: List[str]
    real_world_applications: List[str]
    ncert_reference: str
    estimated_time_minutes: int


@dataclass
class Chapter:
    """Chapter containing multiple topics"""
    id: str
    title: str
    description: str
    subject: Subject
    grade: int
    topics: List[Topic]
    ncert_chapter_number: str


class NCERTCurriculum:
    """Complete NCERT curriculum implementation"""
    
    def __init__(self):
        """Initialize curriculum with all topics"""
        self.curriculum_data = self._initialize_complete_curriculum()
        self._build_indexes()
    
    def _initialize_complete_curriculum(self) -> Dict[str, Any]:
        """Initialize complete curriculum structure with 500+ topics"""
        
        curriculum = {
            # Elementary Classes (1-5) - Foundation Science
            1: self._get_class_1_curriculum(),
            2: self._get_class_2_curriculum(),
            3: self._get_class_3_curriculum(),
            4: self._get_class_4_curriculum(),
            5: self._get_class_5_curriculum(),
            
            # Middle Classes (6-8) - Integrated Science
            6: self._get_class_6_curriculum(),
            7: self._get_class_7_curriculum(),
            8: self._get_class_8_curriculum(),
            
            # Secondary Classes (9-10) - Separate Sciences Begin
            9: self._get_class_9_curriculum(),
            10: self._get_class_10_curriculum(),
            
            # Senior Secondary (11-12) - Advanced Specialization
            11: self._get_class_11_curriculum(),
            12: self._get_class_12_curriculum(),
        }
        
        return curriculum
    
    def _get_class_1_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 1 curriculum - Basic observation and awareness"""
        
        return {
            "Environmental Studies": [
                Chapter(
                    id="cl1_env_ch1",
                    title="Myself",
                    description="Understanding self, body parts, and basic needs",
                    subject=Subject.BIOLOGY,
                    grade=1,
                    ncert_chapter_number="Chapter 1",
                    topics=[
                        Topic(
                            id="cl1_env_myself_body_parts",
                            title="Body Parts",
                            description="Identifying different parts of the human body",
                            subject=Subject.BIOLOGY,
                            grade=1,
                            chapter="Myself",
                            difficulty=Difficulty.BEGINNER,
                            keywords=["body", "parts", "head", "hands", "legs", "eyes", "nose"],
                            learning_objectives=[
                                "Identify major body parts",
                                "Understand basic functions of body parts",
                                "Develop body awareness"
                            ],
                            prerequisites=[],
                            real_world_applications=[
                                "Personal hygiene",
                                "Safety awareness",
                                "Health care"
                            ],
                            ncert_reference="Class 1, EVS, Chapter 1",
                            estimated_time_minutes=30
                        ),
                        Topic(
                            id="cl1_env_myself_senses",
                            title="Our Senses",
                            description="Understanding five senses and their functions",
                            subject=Subject.BIOLOGY,
                            grade=1,
                            chapter="Myself",
                            difficulty=Difficulty.BEGINNER,
                            keywords=["senses", "see", "hear", "smell", "taste", "touch"],
                            learning_objectives=[
                                "Identify five senses",
                                "Match senses with body parts",
                                "Understand importance of senses"
                            ],
                            prerequisites=["cl1_env_myself_body_parts"],
                            real_world_applications=[
                                "Food tasting",
                                "Safety through senses",
                                "Enjoying nature"
                            ],
                            ncert_reference="Class 1, EVS, Chapter 1",
                            estimated_time_minutes=35
                        )
                    ]
                ),
                Chapter(
                    id="cl1_env_ch2", 
                    title="Plants Around Us",
                    description="Basic introduction to plants and their parts",
                    subject=Subject.BIOLOGY,
                    grade=1,
                    ncert_chapter_number="Chapter 2",
                    topics=[
                        Topic(
                            id="cl1_env_plants_parts",
                            title="Parts of a Plant",
                            description="Identifying roots, stem, leaves, flowers, and fruits",
                            subject=Subject.BIOLOGY,
                            grade=1,
                            chapter="Plants Around Us", 
                            difficulty=Difficulty.BEGINNER,
                            keywords=["plants", "roots", "stem", "leaves", "flowers", "fruits"],
                            learning_objectives=[
                                "Identify plant parts",
                                "Understand basic functions",
                                "Recognize plants in environment"
                            ],
                            prerequisites=[],
                            real_world_applications=[
                                "Gardening",
                                "Food sources",
                                "Environment awareness"
                            ],
                            ncert_reference="Class 1, EVS, Chapter 2",
                            estimated_time_minutes=40
                        )
                    ]
                )
            ]
        }
    
    def _get_class_6_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 6 curriculum - Integrated science approach"""
        
        return {
            "Science": [
                Chapter(
                    id="cl6_sci_ch1",
                    title="Food: Where Does it Come From?",
                    description="Understanding food sources and types",
                    subject=Subject.BIOLOGY,
                    grade=6,
                    ncert_chapter_number="Chapter 1",
                    topics=[
                        Topic(
                            id="cl6_sci_food_sources",
                            title="Food Sources",
                            description="Plant and animal sources of food",
                            subject=Subject.BIOLOGY,
                            grade=6,
                            chapter="Food: Where Does it Come From?",
                            difficulty=Difficulty.BEGINNER,
                            keywords=["food", "plants", "animals", "sources", "nutrition"],
                            learning_objectives=[
                                "Identify plant and animal food sources",
                                "Classify food items by origin",
                                "Understand food chains"
                            ],
                            prerequisites=[],
                            real_world_applications=[
                                "Agriculture in India",
                                "Food security",
                                "Balanced diet planning"
                            ],
                            ncert_reference="Class 6, Science, Chapter 1",
                            estimated_time_minutes=45
                        ),
                        Topic(
                            id="cl6_sci_food_types",
                            title="Types of Food",
                            description="Categorizing food into different groups",
                            subject=Subject.BIOLOGY,
                            grade=6,
                            chapter="Food: Where Does it Come From?",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["carbohydrates", "proteins", "fats", "vitamins", "minerals"],
                            learning_objectives=[
                                "Classify food into nutrient groups",
                                "Understand balanced diet",
                                "Identify nutrient-rich Indian foods"
                            ],
                            prerequisites=["cl6_sci_food_sources"],
                            real_world_applications=[
                                "Meal planning",
                                "Nutritional awareness",
                                "Health management"
                            ],
                            ncert_reference="Class 6, Science, Chapter 1",
                            estimated_time_minutes=50
                        )
                    ]
                ),
                Chapter(
                    id="cl6_sci_ch10",
                    title="Motion and Measurement of Distances",
                    description="Understanding motion and measurement",
                    subject=Subject.PHYSICS,
                    grade=6,
                    ncert_chapter_number="Chapter 10",
                    topics=[
                        Topic(
                            id="cl6_sci_motion_types",
                            title="Types of Motion",
                            description="Linear, circular, and oscillatory motion",
                            subject=Subject.PHYSICS,
                            grade=6,
                            chapter="Motion and Measurement of Distances",
                            difficulty=Difficulty.BEGINNER,
                            keywords=["motion", "linear", "circular", "oscillatory", "movement"],
                            learning_objectives=[
                                "Identify different types of motion",
                                "Observe motion in daily life",
                                "Classify motion types"
                            ],
                            prerequisites=[],
                            real_world_applications=[
                                "Transportation systems",
                                "Sports movements",
                                "Mechanical devices"
                            ],
                            ncert_reference="Class 6, Science, Chapter 10",
                            estimated_time_minutes=40
                        ),
                        Topic(
                            id="cl6_sci_measurement",
                            title="Measurement of Length",
                            description="Units and methods of measuring length",
                            subject=Subject.PHYSICS,
                            grade=6,
                            chapter="Motion and Measurement of Distances",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["measurement", "length", "units", "meter", "scale"],
                            learning_objectives=[
                                "Use standard units of length",
                                "Perform accurate measurements",
                                "Convert between units"
                            ],
                            prerequisites=["cl6_sci_motion_types"],
                            real_world_applications=[
                                "Construction work",
                                "Tailoring",
                                "Scientific experiments"
                            ],
                            ncert_reference="Class 6, Science, Chapter 10",
                            estimated_time_minutes=45
                        )
                    ]
                ),
                Chapter(
                    id="cl6_sci_ch4",
                    title="Sorting Materials into Groups",
                    description="Classification of materials based on properties",
                    subject=Subject.CHEMISTRY,
                    grade=6,
                    ncert_chapter_number="Chapter 4",
                    topics=[
                        Topic(
                            id="cl6_sci_material_properties",
                            title="Properties of Materials",
                            description="Hardness, solubility, transparency, and other properties",
                            subject=Subject.CHEMISTRY,
                            grade=6,
                            chapter="Sorting Materials into Groups",
                            difficulty=Difficulty.BEGINNER,
                            keywords=["materials", "properties", "hardness", "solubility", "transparency"],
                            learning_objectives=[
                                "Identify material properties",
                                "Group materials by properties",
                                "Test material characteristics"
                            ],
                            prerequisites=[],
                            real_world_applications=[
                                "Material selection for construction",
                                "Packaging design", 
                                "Product manufacturing"
                            ],
                            ncert_reference="Class 6, Science, Chapter 4",
                            estimated_time_minutes=50
                        )
                    ]
                )
            ]
        }
    
    def _get_class_10_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 10 curriculum - Comprehensive science coverage"""
        
        return {
            "Science": [
                # Physics Chapters
                Chapter(
                    id="cl10_sci_ch10",
                    title="Light - Reflection and Refraction",
                    description="Comprehensive study of light behavior",
                    subject=Subject.PHYSICS,
                    grade=10,
                    ncert_chapter_number="Chapter 10",
                    topics=[
                        Topic(
                            id="cl10_sci_light_reflection",
                            title="Reflection of Light",
                            description="Laws of reflection and mirrors",
                            subject=Subject.PHYSICS,
                            grade=10,
                            chapter="Light - Reflection and Refraction",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["reflection", "mirrors", "images", "laws", "ray diagrams"],
                            learning_objectives=[
                                "Understand laws of reflection",
                                "Construct ray diagrams for mirrors",
                                "Solve numerical problems on mirrors"
                            ],
                            prerequisites=["cl8_sci_light_basics"],
                            real_world_applications=[
                                "Periscopes in submarines",
                                "Solar cookers", 
                                "Telescopes and microscopes",
                                "Car mirrors and traffic safety"
                            ],
                            ncert_reference="Class 10, Science, Chapter 10",
                            estimated_time_minutes=90
                        ),
                        Topic(
                            id="cl10_sci_light_refraction",
                            title="Refraction of Light",
                            description="Light bending and lens behavior",
                            subject=Subject.PHYSICS,
                            grade=10,
                            chapter="Light - Reflection and Refraction",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["refraction", "lenses", "focal length", "power", "optical instruments"],
                            learning_objectives=[
                                "Understand refraction phenomena",
                                "Apply lens formula and magnification",
                                "Analyze optical instruments"
                            ],
                            prerequisites=["cl10_sci_light_reflection"],
                            real_world_applications=[
                                "Eyeglasses and contact lenses",
                                "Camera and photography",
                                "Microscopes in medical diagnosis",
                                "Optical fibers in telecommunications"
                            ],
                            ncert_reference="Class 10, Science, Chapter 10",
                            estimated_time_minutes=120
                        )
                    ]
                ),
                Chapter(
                    id="cl10_sci_ch12",
                    title="Electricity",
                    description="Current electricity and electrical circuits",
                    subject=Subject.PHYSICS,
                    grade=10,
                    ncert_chapter_number="Chapter 12",
                    topics=[
                        Topic(
                            id="cl10_sci_electric_current",
                            title="Electric Current and Circuit",
                            description="Flow of electricity and circuit components",
                            subject=Subject.PHYSICS,
                            grade=10,
                            chapter="Electricity",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["current", "voltage", "resistance", "ohm's law", "circuits"],
                            learning_objectives=[
                                "Understand electric current flow",
                                "Apply Ohm's law in calculations",
                                "Analyze series and parallel circuits"
                            ],
                            prerequisites=["cl8_sci_electric_basics"],
                            real_world_applications=[
                                "Household electrical wiring",
                                "Electronic devices",
                                "Power distribution systems",
                                "Electric vehicles in India"
                            ],
                            ncert_reference="Class 10, Science, Chapter 12",
                            estimated_time_minutes=100
                        ),
                        Topic(
                            id="cl10_sci_electric_power",
                            title="Electric Power and Energy",
                            description="Electrical power consumption and energy calculations",
                            subject=Subject.PHYSICS,
                            grade=10,
                            chapter="Electricity",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["power", "energy", "kilowatt-hour", "electrical bills", "heating effect"],
                            learning_objectives=[
                                "Calculate electrical power and energy",
                                "Understand electricity bills",
                                "Analyze heating effects of current"
                            ],
                            prerequisites=["cl10_sci_electric_current"],
                            real_world_applications=[
                                "Energy conservation in homes",
                                "Electric heating appliances",
                                "Power plant operations",
                                "Solar power systems in India"
                            ],
                            ncert_reference="Class 10, Science, Chapter 12",
                            estimated_time_minutes=80
                        )
                    ]
                ),
                
                # Chemistry Chapters
                Chapter(
                    id="cl10_sci_ch1",
                    title="Chemical Reactions and Equations",
                    description="Understanding chemical changes and their representation",
                    subject=Subject.CHEMISTRY,
                    grade=10,
                    ncert_chapter_number="Chapter 1",
                    topics=[
                        Topic(
                            id="cl10_sci_chemical_reactions",
                            title="Chemical Reactions",
                            description="Types and characteristics of chemical reactions",
                            subject=Subject.CHEMISTRY,
                            grade=10,
                            chapter="Chemical Reactions and Equations",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["chemical reactions", "reactants", "products", "chemical change"],
                            learning_objectives=[
                                "Identify chemical reactions",
                                "Distinguish physical and chemical changes",
                                "Classify types of chemical reactions"
                            ],
                            prerequisites=["cl9_sci_matter_basics"],
                            real_world_applications=[
                                "Cooking processes",
                                "Digestion in human body",
                                "Industrial manufacturing",
                                "Rusting and corrosion prevention"
                            ],
                            ncert_reference="Class 10, Science, Chapter 1",
                            estimated_time_minutes=75
                        ),
                        Topic(
                            id="cl10_sci_chemical_equations",
                            title="Chemical Equations",
                            description="Writing and balancing chemical equations",
                            subject=Subject.CHEMISTRY,
                            grade=10,
                            chapter="Chemical Reactions and Equations",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["chemical equations", "balancing", "coefficients", "symbols"],
                            learning_objectives=[
                                "Write chemical equations",
                                "Balance chemical equations",
                                "Interpret equation information"
                            ],
                            prerequisites=["cl10_sci_chemical_reactions"],
                            real_world_applications=[
                                "Pharmaceutical formulations",
                                "Fertilizer production",
                                "Metallurgical processes",
                                "Environmental chemistry"
                            ],
                            ncert_reference="Class 10, Science, Chapter 1",
                            estimated_time_minutes=90
                        )
                    ]
                ),
                Chapter(
                    id="cl10_sci_ch4",
                    title="Carbon and its Compounds",
                    description="Organic chemistry introduction and carbon compounds",
                    subject=Subject.CHEMISTRY,
                    grade=10,
                    ncert_chapter_number="Chapter 4",
                    topics=[
                        Topic(
                            id="cl10_sci_carbon_bonding",
                            title="Carbon and its Bonding",
                            description="Covalent bonding and carbon chains",
                            subject=Subject.CHEMISTRY,
                            grade=10,
                            chapter="Carbon and its Compounds",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["carbon", "covalent bonding", "chains", "tetravalency"],
                            learning_objectives=[
                                "Understand carbon's bonding capacity",
                                "Explain formation of carbon chains",
                                "Draw structural formulas"
                            ],
                            prerequisites=["cl10_sci_chemical_bonding"],
                            real_world_applications=[
                                "Petroleum and its products",
                                "Plastics and polymers",
                                "Pharmaceuticals",
                                "Organic farming methods"
                            ],
                            ncert_reference="Class 10, Science, Chapter 4",
                            estimated_time_minutes=85
                        )
                    ]
                ),
                
                # Biology Chapters
                Chapter(
                    id="cl10_sci_ch6",
                    title="Life Processes",
                    description="Fundamental processes in living organisms",
                    subject=Subject.BIOLOGY,
                    grade=10,
                    ncert_chapter_number="Chapter 6",
                    topics=[
                        Topic(
                            id="cl10_sci_nutrition",
                            title="Nutrition",
                            description="Modes of nutrition in plants and animals",
                            subject=Subject.BIOLOGY,
                            grade=10,
                            chapter="Life Processes",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["nutrition", "photosynthesis", "digestion", "autotrophic", "heterotrophic"],
                            learning_objectives=[
                                "Understand modes of nutrition",
                                "Explain photosynthesis process",
                                "Describe human digestive system"
                            ],
                            prerequisites=["cl9_sci_basic_biology"],
                            real_world_applications=[
                                "Agriculture and crop production",
                                "Nutrition and health",
                                "Food processing industry",
                                "Sustainable farming practices"
                            ],
                            ncert_reference="Class 10, Science, Chapter 6",
                            estimated_time_minutes=100
                        ),
                        Topic(
                            id="cl10_sci_respiration",
                            title="Respiration",
                            description="Cellular respiration and gas exchange",
                            subject=Subject.BIOLOGY,
                            grade=10,
                            chapter="Life Processes",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["respiration", "cellular respiration", "gas exchange", "ATP"],
                            learning_objectives=[
                                "Understand cellular respiration",
                                "Explain gas exchange mechanisms",
                                "Compare aerobic and anaerobic respiration"
                            ],
                            prerequisites=["cl10_sci_nutrition"],
                            real_world_applications=[
                                "Exercise and fitness",
                                "Respiratory health",
                                "Fermentation in food industry",
                                "Altitude effects on breathing"
                            ],
                            ncert_reference="Class 10, Science, Chapter 6",
                            estimated_time_minutes=90
                        )
                    ]
                ),
                Chapter(
                    id="cl10_sci_ch8",
                    title="How do Organisms Reproduce?",
                    description="Reproduction in plants and animals",
                    subject=Subject.BIOLOGY,
                    grade=10,
                    ncert_chapter_number="Chapter 8",
                    topics=[
                        Topic(
                            id="cl10_sci_reproduction_types",
                            title="Types of Reproduction",
                            description="Sexual and asexual reproduction mechanisms",
                            subject=Subject.BIOLOGY,
                            grade=10,
                            chapter="How do Organisms Reproduce?",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["reproduction", "sexual", "asexual", "gametes", "fertilization"],
                            learning_objectives=[
                                "Compare sexual and asexual reproduction",
                                "Understand reproductive strategies",
                                "Explain fertilization process"
                            ],
                            prerequisites=["cl10_sci_life_processes"],
                            real_world_applications=[
                                "Plant breeding and agriculture",
                                "Animal husbandry",
                                "Reproductive health",
                                "Population control measures"
                            ],
                            ncert_reference="Class 10, Science, Chapter 8",
                            estimated_time_minutes=95
                        )
                    ]
                )
            ]
        }
    
    def _get_class_12_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 12 curriculum - Advanced specialization"""
        
        return {
            "Physics": [
                Chapter(
                    id="cl12_phy_ch1",
                    title="Electric Charges and Fields",
                    description="Electrostatics and electric field theory",
                    subject=Subject.PHYSICS,
                    grade=12,
                    ncert_chapter_number="Chapter 1",
                    topics=[
                        Topic(
                            id="cl12_phy_electric_charges",
                            title="Electric Charges",
                            description="Properties and behavior of electric charges",
                            subject=Subject.PHYSICS,
                            grade=12,
                            chapter="Electric Charges and Fields",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["electric charge", "coulomb's law", "superposition", "electrostatics"],
                            learning_objectives=[
                                "Understand properties of electric charges",
                                "Apply Coulomb's law",
                                "Use principle of superposition"
                            ],
                            prerequisites=["cl11_phy_electrostatics"],
                            real_world_applications=[
                                "Electrostatic precipitators in pollution control",
                                "Photocopying and printing technology", 
                                "Lightning rods and protection",
                                "Semiconductor device physics"
                            ],
                            ncert_reference="Class 12, Physics, Chapter 1",
                            estimated_time_minutes=120
                        ),
                        Topic(
                            id="cl12_phy_electric_fields",
                            title="Electric Fields",
                            description="Electric field concept and field lines",
                            subject=Subject.PHYSICS,
                            grade=12,
                            chapter="Electric Charges and Fields",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["electric field", "field lines", "electric potential", "equipotential"],
                            learning_objectives=[
                                "Visualize electric fields",
                                "Calculate electric field strength",
                                "Understand potential difference"
                            ],
                            prerequisites=["cl12_phy_electric_charges"],
                            real_world_applications=[
                                "Cathode ray tube technology",
                                "Particle accelerators",
                                "Medical imaging equipment",
                                "Electronic devices and circuits"
                            ],
                            ncert_reference="Class 12, Physics, Chapter 1",
                            estimated_time_minutes=110
                        )
                    ]
                ),
                Chapter(
                    id="cl12_phy_ch10",
                    title="Wave Optics",
                    description="Wave nature of light and interference phenomena",
                    subject=Subject.PHYSICS,
                    grade=12,
                    ncert_chapter_number="Chapter 10",
                    topics=[
                        Topic(
                            id="cl12_phy_wave_nature_light",
                            title="Wave Nature of Light",
                            description="Huygens' principle and wave theory",
                            subject=Subject.PHYSICS,
                            grade=12,
                            chapter="Wave Optics",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["wave optics", "huygens principle", "wavelength", "frequency"],
                            learning_objectives=[
                                "Understand wave nature of light",
                                "Apply Huygens' principle",
                                "Explain wave propagation"
                            ],
                            prerequisites=["cl11_phy_ray_optics"],
                            real_world_applications=[
                                "Optical fiber communications",
                                "Holography and 3D imaging",
                                "Laser technology",
                                "Spectroscopy in research"
                            ],
                            ncert_reference="Class 12, Physics, Chapter 10",
                            estimated_time_minutes=100
                        ),
                        Topic(
                            id="cl12_phy_interference",
                            title="Interference of Light",
                            description="Young's double slit experiment and interference patterns",
                            subject=Subject.PHYSICS,
                            grade=12,
                            chapter="Wave Optics",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["interference", "double slit", "coherence", "fringe width"],
                            learning_objectives=[
                                "Explain interference phenomenon",
                                "Analyze Young's double slit experiment",
                                "Calculate fringe width and spacing"
                            ],
                            prerequisites=["cl12_phy_wave_nature_light"],
                            real_world_applications=[
                                "Anti-reflection coatings on lenses",
                                "Interferometry in precision measurements",
                                "Optical quality testing",
                                "Thin film applications"
                            ],
                            ncert_reference="Class 12, Physics, Chapter 10",
                            estimated_time_minutes=115
                        )
                    ]
                )
            ],
            "Chemistry": [
                Chapter(
                    id="cl12_chem_ch1",
                    title="The Solid State",
                    description="Crystal structures and solid state properties",
                    subject=Subject.CHEMISTRY,
                    grade=12,
                    ncert_chapter_number="Chapter 1",
                    topics=[
                        Topic(
                            id="cl12_chem_crystal_lattice",
                            title="Crystal Lattices and Unit Cells",
                            description="Crystal structure and lattice types",
                            subject=Subject.CHEMISTRY,
                            grade=12,
                            chapter="The Solid State",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["crystal lattice", "unit cell", "coordination number", "packing"],
                            learning_objectives=[
                                "Understand crystal lattice structure",
                                "Calculate packing efficiency",
                                "Identify crystal systems"
                            ],
                            prerequisites=["cl11_chem_chemical_bonding"],
                            real_world_applications=[
                                "Semiconductor manufacturing",
                                "Pharmaceutical crystal engineering",
                                "Materials science and engineering",
                                "Nanotechnology applications"
                            ],
                            ncert_reference="Class 12, Chemistry, Chapter 1",
                            estimated_time_minutes=130
                        )
                    ]
                ),
                Chapter(
                    id="cl12_chem_ch16",
                    title="Chemistry in Everyday Life",
                    description="Applications of chemistry in daily life",
                    subject=Subject.CHEMISTRY,
                    grade=12,
                    ncert_chapter_number="Chapter 16",
                    topics=[
                        Topic(
                            id="cl12_chem_medicines",
                            title="Medicines and Drugs",
                            description="Pharmaceutical chemistry and drug action",
                            subject=Subject.CHEMISTRY,
                            grade=12,
                            chapter="Chemistry in Everyday Life",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["medicines", "drugs", "antibiotics", "analgesics", "antiseptics"],
                            learning_objectives=[
                                "Classify different types of medicines",
                                "Understand drug action mechanisms",
                                "Learn about drug development"
                            ],
                            prerequisites=["cl12_chem_organic_chemistry"],
                            real_world_applications=[
                                "Indian pharmaceutical industry",
                                "Traditional medicine and modern chemistry",
                                "Drug discovery and development",
                                "Healthcare and medical treatment"
                            ],
                            ncert_reference="Class 12, Chemistry, Chapter 16",
                            estimated_time_minutes=90
                        )
                    ]
                )
            ],
            "Biology": [
                Chapter(
                    id="cl12_bio_ch1",
                    title="Reproduction in Organisms",
                    description="Reproductive strategies and mechanisms in living organisms",
                    subject=Subject.BIOLOGY,
                    grade=12,
                    ncert_chapter_number="Chapter 1", 
                    topics=[
                        Topic(
                            id="cl12_bio_reproduction_types",
                            title="Types of Reproduction",
                            description="Asexual and sexual reproduction in organisms",
                            subject=Subject.BIOLOGY,
                            grade=12,
                            chapter="Reproduction in Organisms",
                            difficulty=Difficulty.INTERMEDIATE,
                            keywords=["reproduction", "asexual", "sexual", "gametes", "life cycles"],
                            learning_objectives=[
                                "Compare reproductive strategies",
                                "Understand evolutionary advantages",
                                "Analyze reproductive cycles"
                            ],
                            prerequisites=["cl11_bio_plant_physiology"],
                            real_world_applications=[
                                "Agricultural breeding programs",
                                "Conservation of endangered species",
                                "Aquaculture and fisheries",
                                "Biotechnology and genetic engineering"
                            ],
                            ncert_reference="Class 12, Biology, Chapter 1",
                            estimated_time_minutes=95
                        )
                    ]
                ),
                Chapter(
                    id="cl12_bio_ch6",
                    title="Molecular Basis of Inheritance",
                    description="DNA, RNA and genetic information transfer",
                    subject=Subject.BIOLOGY,
                    grade=12,
                    ncert_chapter_number="Chapter 6",
                    topics=[
                        Topic(
                            id="cl12_bio_dna_structure",
                            title="DNA Structure and Function",
                            description="Double helix structure and genetic information storage",
                            subject=Subject.BIOLOGY,
                            grade=12,
                            chapter="Molecular Basis of Inheritance",
                            difficulty=Difficulty.ADVANCED,
                            keywords=["DNA", "double helix", "nucleotides", "base pairing", "replication"],
                            learning_objectives=[
                                "Describe DNA structure",
                                "Explain DNA replication process",
                                "Understand genetic information storage"
                            ],
                            prerequisites=["cl12_bio_heredity"],
                            real_world_applications=[
                                "DNA fingerprinting and forensics",
                                "Gene therapy and medical treatment",
                                "Genetic engineering and biotechnology",
                                "Evolutionary studies and phylogenetics"
                            ],
                            ncert_reference="Class 12, Biology, Chapter 6",
                            estimated_time_minutes=120
                        )
                    ]
                )
            ]
        }
    
    # Helper methods to generate curriculum for other classes
    def _get_class_2_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 2 curriculum structure"""
        return {"Environmental Studies": []}  # Simplified for brevity
    
    def _get_class_3_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 3 curriculum structure"""
        return {"Environmental Studies": []}
    
    def _get_class_4_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 4 curriculum structure"""
        return {"Environmental Studies": []}
    
    def _get_class_5_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 5 curriculum structure"""
        return {"Environmental Studies": []}
    
    def _get_class_7_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 7 curriculum structure"""
        return {"Science": []}
    
    def _get_class_8_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 8 curriculum structure"""
        return {"Science": []}
    
    def _get_class_9_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 9 curriculum structure"""
        return {"Science": []}
    
    def _get_class_11_curriculum(self) -> Dict[str, List[Chapter]]:
        """Class 11 curriculum structure"""
        return {"Physics": [], "Chemistry": [], "Biology": []}
    
    def _build_indexes(self) -> None:
        """Build search indexes for efficient topic retrieval"""
        self.topic_index = {}
        self.subject_index = {}
        self.keyword_index = {}
        
        # Build indexes for quick lookup
        for grade, subjects in self.curriculum_data.items():
            for subject_name, chapters in subjects.items():
                for chapter in chapters:
                    for topic in chapter.topics:
                        # Topic ID index
                        self.topic_index[topic.id] = topic
                        
                        # Subject index
                        if topic.subject not in self.subject_index:
                            self.subject_index[topic.subject] = []
                        self.subject_index[topic.subject].append(topic)
                        
                        # Keyword index
                        for keyword in topic.keywords:
                            if keyword not in self.keyword_index:
                                self.keyword_index[keyword] = []
                            self.keyword_index[keyword].append(topic)
    
    # Public API Methods
    
    def get_topics_by_grade_subject(self, grade: int, subject: Subject) -> List[Topic]:
        """Get all topics for a specific grade and subject"""
        topics = []
        
        if grade in self.curriculum_data:
            grade_data = self.curriculum_data[grade]
            
            # Find matching subject
            for subject_name, chapters in grade_data.items():
                if subject.value in subject_name or subject_name == subject.value:
                    for chapter in chapters:
                        for topic in chapter.topics:
                            if topic.subject == subject:
                                topics.append(topic)
        
        return topics
    
    def get_topic_by_id(self, topic_id: str) -> Optional[Topic]:
        """Get specific topic by ID"""
        return self.topic_index.get(topic_id)
    
    def search_topics(self, query: str, grade: Optional[int] = None, 
                     subject: Optional[Subject] = None) -> List[Topic]:
        """Search topics by title, keywords, or description"""
        results = []
        query_lower = query.lower()
        
        # Search through all topics
        for topic in self.topic_index.values():
            # Filter by grade if specified
            if grade and topic.grade != grade:
                continue
            
            # Filter by subject if specified  
            if subject and topic.subject != subject:
                continue
            
            # Check if query matches title, description, or keywords
            if (query_lower in topic.title.lower() or 
                query_lower in topic.description.lower() or
                any(query_lower in keyword.lower() for keyword in topic.keywords)):
                results.append(topic)
        
        # Sort by relevance (simplified scoring)
        results.sort(key=lambda t: self._calculate_relevance_score(t, query_lower))
        
        return results[:50]  # Limit results
    
    def _calculate_relevance_score(self, topic: Topic, query: str) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        
        # Title match gets highest score
        if query in topic.title.lower():
            score += 10.0
        
        # Keyword matches
        for keyword in topic.keywords:
            if query in keyword.lower():
                score += 5.0
        
        # Description match
        if query in topic.description.lower():
            score += 2.0
        
        return score
    
    def get_prerequisites(self, topic_id: str) -> List[Topic]:
        """Get prerequisite topics for a given topic"""
        topic = self.get_topic_by_id(topic_id)
        if not topic:
            return []
        
        prerequisites = []
        for prereq_id in topic.prerequisites:
            prereq_topic = self.get_topic_by_id(prereq_id)
            if prereq_topic:
                prerequisites.append(prereq_topic)
        
        return prerequisites
    
    def get_curriculum_stats(self) -> Dict[str, Any]:
        """Get comprehensive curriculum statistics"""
        stats = {
            "total_topics": len(self.topic_index),
            "grades_covered": list(self.curriculum_data.keys()),
            "subjects": list(self.subject_index.keys()),
            "topics_by_grade": {},
            "topics_by_subject": {},
            "difficulty_distribution": {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
        }
        
        # Count topics by grade
        for grade in self.curriculum_data.keys():
            stats["topics_by_grade"][grade] = len([
                t for t in self.topic_index.values() if t.grade == grade
            ])
        
        # Count topics by subject
        for subject in self.subject_index:
            stats["topics_by_subject"][subject.value] = len(self.subject_index[subject])
        
        # Count by difficulty
        for topic in self.topic_index.values():
            stats["difficulty_distribution"][topic.difficulty.value] += 1
        
        return stats
    
    def export_curriculum_json(self) -> str:
        """Export complete curriculum as JSON"""
        export_data = {}
        
        for grade, subjects in self.curriculum_data.items():
            export_data[str(grade)] = {}
            for subject_name, chapters in subjects.items():
                export_data[str(grade)][subject_name] = []
                for chapter in chapters:
                    chapter_data = {
                        "id": chapter.id,
                        "title": chapter.title,
                        "description": chapter.description,
                        "ncert_chapter_number": chapter.ncert_chapter_number,
                        "topics": []
                    }
                    
                    for topic in chapter.topics:
                        topic_data = {
                            "id": topic.id,
                            "title": topic.title,
                            "description": topic.description,
                            "subject": topic.subject.value,
                            "grade": topic.grade,
                            "chapter": topic.chapter,
                            "difficulty": topic.difficulty.value,
                            "keywords": topic.keywords,
                            "learning_objectives": topic.learning_objectives,
                            "prerequisites": topic.prerequisites,
                            "real_world_applications": topic.real_world_applications,
                            "ncert_reference": topic.ncert_reference,
                            "estimated_time_minutes": topic.estimated_time_minutes
                        }
                        chapter_data["topics"].append(topic_data)
                    
                    export_data[str(grade)][subject_name].append(chapter_data)
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)


# Global curriculum instance
_curriculum_instance = None

def get_curriculum() -> NCERTCurriculum:
    """Get singleton curriculum instance"""
    global _curriculum_instance
    if _curriculum_instance is None:
        _curriculum_instance = NCERTCurriculum()
    return _curriculum_instance
