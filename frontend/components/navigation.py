"""
Advanced Navigation Component for ScienceGPT v3.0
Modern navigation with icons, progress indicators, and analytics
"""

import streamlit as st
from streamlit_option_menu import option_menu
from typing import Dict, Any, Optional
import time

from backend.database.db_manager import get_database_manager
from backend.utils.analytics import track_navigation_event


class NavigationManager:
    """Manages navigation state and user flow"""
    
    def __init__(self):
        """Initialize navigation manager"""
        self.pages = {
            "home": {
                "title": "Home", 
                "icon": "🏠",
                "description": "Dashboard and overview",
                "requires_auth": False
            },
            "learn": {
                "title": "Learn",
                "icon": "🧠", 
                "description": "Interactive AI learning",
                "requires_auth": False
            },
            "practice": {
                "title": "Practice",
                "icon": "📝",
                "description": "Quizzes and exercises", 
                "requires_auth": False
            },
            "curriculum": {
                "title": "Curriculum",
                "icon": "📚",
                "description": "NCERT topic explorer",
                "requires_auth": False
            },
            "progress": {
                "title": "Progress", 
                "icon": "📊",
                "description": "Learning analytics",
                "requires_auth": False
            },
            "achievements": {
                "title": "Achievements",
                "icon": "🏆", 
                "description": "Badges and rewards",
                "requires_auth": False
            },
            "settings": {
                "title": "Settings",
                "icon": "⚙️",
                "description": "Preferences and profile",
                "requires_auth": False
            }
        }
    
    def get_user_progress_indicator(self) -> Dict[str, float]:
        """Get progress indicators for each section"""
        
        # Get user's current progress from session state
        total_points = st.session_state.get('points', 0)
        quizzes_completed = st.session_state.get('quizzes_completed', 0)
        topics_studied = st.session_state.get('topics_studied', 0)
        achievements_earned = len(st.session_state.get('badges', []))
        
        return {
            "learn": min(100, (topics_studied / 50) * 100),  # Assume 50 topics target
            "practice": min(100, (quizzes_completed / 20) * 100),  # Assume 20 quiz target
            "curriculum": min(100, (topics_studied / 100) * 100),  # Curriculum exploration
            "progress": min(100, (total_points / 500) * 100),  # Points target
            "achievements": min(100, (achievements_earned / 10) * 100),  # Badge target
            "home": min(100, ((total_points + quizzes_completed + topics_studied) / 100) * 100)
        }


def render_navigation() -> str:
    """Render modern navigation component with progress indicators"""
    
    nav_manager = NavigationManager()
    progress_indicators = nav_manager.get_user_progress_indicator()
    
    # Custom CSS for navigation
    st.markdown("""
    <style>
    .nav-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .nav-progress {
        background: rgba(255, 255, 255, 0.2);
        height: 4px;
        border-radius: 2px;
        margin-top: 0.5rem;
        overflow: hidden;
    }
    
    .nav-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        border-radius: 2px;
        transition: width 0.3s ease;
    }
    
    .nav-stats {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
        color: white;
        font-size: 0.8rem;
    }
    
    .nav-stat {
        text-align: center;
        opacity: 0.9;
    }
    
    .nav-stat-value {
        font-weight: bold;
        font-size: 1.2rem;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main navigation menu
    with st.container():
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # Navigation menu
        selected = option_menu(
            menu_title="ScienceGPT v3.0",
            options=[nav_manager.pages[key]["title"] for key in nav_manager.pages.keys()],
            icons=[nav_manager.pages[key]["icon"] for key in nav_manager.pages.keys()],
            menu_icon="🧪",
            default_index=list(nav_manager.pages.keys()).index(st.session_state.get('current_page', 'home')),
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0",
                    "background-color": "transparent",
                    "border": "none"
                },
                "icon": {
                    "color": "white", 
                    "font-size": "1.2rem"
                },
                "nav-link": {
                    "font-size": "0.9rem",
                    "text-align": "center",
                    "margin": "0 0.5rem",
                    "color": "white",
                    "background-color": "transparent",
                    "border-radius": "10px",
                    "padding": "0.5rem 1rem"
                },
                "nav-link-selected": {
                    "background-color": "rgba(255, 255, 255, 0.2)",
                    "color": "white",
                    "font-weight": "bold"
                }
            }
        )
        
        # Convert selected title back to key
        selected_key = None
        for key, page_data in nav_manager.pages.items():
            if page_data["title"] == selected:
                selected_key = key
                break
        
        # Progress indicator for selected page
        if selected_key in progress_indicators:
            progress = progress_indicators[selected_key]
            st.markdown(f"""
            <div class="nav-progress">
                <div class="nav-progress-fill" style="width: {progress}%"></div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick stats
        total_points = st.session_state.get('points', 0)
        streak = st.session_state.get('streak', 0)
        level = st.session_state.get('level', 'Beginner')
        
        st.markdown(f"""
        <div class="nav-stats">
            <div class="nav-stat">
                <span class="nav-stat-value">{total_points}</span>
                <span>Points</span>
            </div>
            <div class="nav-stat">
                <span class="nav-stat-value">{streak}</span>
                <span>Day Streak</span>
            </div>
            <div class="nav-stat">
                <span class="nav-stat-value">{level}</span>
                <span>Level</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Update session state
        if selected_key:
            st.session_state.current_page = selected_key
            
            # Track navigation analytics
            try:
                track_navigation_event(
                    user_id=st.session_state.get('user_id'),
                    from_page=st.session_state.get('previous_page', 'unknown'),
                    to_page=selected_key,
                    session_time=time.time()
                )
                st.session_state.previous_page = selected_key
            except Exception:
                pass  # Silent fail for analytics
    
    return selected_key or 'home'


def render_breadcrumb(current_page: str, context: Dict[str, Any] = None) -> None:
    """Render breadcrumb navigation for complex pages"""
    
    breadcrumb_paths = {
        "home": ["🏠 Home"],
        "learn": ["🏠 Home", "🧠 Learn"],
        "practice": ["🏠 Home", "📝 Practice"], 
        "curriculum": ["🏠 Home", "📚 Curriculum"],
        "progress": ["🏠 Home", "📊 Progress"],
        "achievements": ["🏠 Home", "🏆 Achievements"],
        "settings": ["🏠 Home", "⚙️ Settings"]
    }
    
    if current_page in breadcrumb_paths:
        path = breadcrumb_paths[current_page]
        
        # Add context if provided
        if context:
            if context.get('subject'):
                path.append(f"📖 {context['subject']}")
            if context.get('topic'):
                path.append(f"📄 {context['topic']}")
        
        breadcrumb_html = " > ".join(path)
        
        st.markdown(f"""
        <div style="
            background: rgba(102, 126, 234, 0.1);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: #4a5568;
        ">
            {breadcrumb_html}
        </div>
        """, unsafe_allow_html=True)


def render_page_header(title: str, description: str, icon: str = "🧪") -> None:
    """Render consistent page header"""
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
    ">
        <h1 style="
            font-size: 2.5rem;
            margin: 0;
            color: #2d3748;
            font-weight: 700;
        ">
            {icon} {title}
        </h1>
        <p style="
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            color: #4a5568;
            opacity: 0.8;
        ">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_quick_actions() -> None:
    """Render quick action buttons in navigation"""
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔥 Daily Challenge", use_container_width=True, type="primary"):
            st.session_state.current_page = "practice"
            st.session_state.quick_action = "daily_challenge"
            st.rerun()
    
    with col2:
        if st.button("🎯 Random Quiz", use_container_width=True):
            st.session_state.current_page = "practice"
            st.session_state.quick_action = "random_quiz"
            st.rerun()
    
    with col3:
        if st.button("📖 Continue Learning", use_container_width=True):
            st.session_state.current_page = "learn"
            st.session_state.quick_action = "continue_learning"
            st.rerun()
