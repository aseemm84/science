"""
ScienceGPT v3.0 - Main Application Entry Point
World-Class AI-Powered Science Education Platform for Indian Students

Features:
- Complete NCERT Curriculum (Classes 1-12, 500+ topics)
- Advanced AI Integration with context awareness
- Premium UI/UX with modern design patterns
- Real-time analytics and progress tracking
- Advanced gamification system
- 50+ concurrent users support
- WCAG 2.1 AA accessibility compliant
- Mobile responsive design

Author: Aseem Mehrotra
Version: 3.0.0
License: MIT
Last Updated: October 17, 2025
"""

import streamlit as st
import sys
import os
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Core imports
from backend.config import AppConfig, get_settings
from backend.database.db_manager import DatabaseManager
from backend.utils.error_handlers import handle_startup_error, log_error
from backend.utils.validators import validate_environment

# Frontend imports
from frontend.components.navigation import render_navigation
from frontend.components.header import render_header
from frontend.components.footer import render_footer
from frontend.components.sidebar import render_sidebar

# Page imports
from frontend.pages import (
    home,
    learn,
    practice,
    progress, 
    achievements,
    curriculum_explorer,
    settings as settings_page
)


class ScienceGPTApp:
    """Main application class for ScienceGPT v3.0"""
    
    def __init__(self):
        """Initialize the ScienceGPT application"""
        self.config = get_settings()
        self.db_manager: Optional[DatabaseManager] = None
        self.initialized = False
    
    def configure_streamlit(self) -> None:
        """Configure Streamlit page settings with premium styling"""
        st.set_page_config(
            page_title="ScienceGPT v3.0 - AI Science Learning Platform",
            page_icon="🧪",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/aseemm84/sciencegpt_v3/wiki',
                'Report a bug': 'https://github.com/aseemm84/sciencegpt_v3/issues/new',
                'About': """
                # 🎓 ScienceGPT v3.0
                
                **World-Class AI-Powered Science Education Platform**
                
                🌟 **Features:**
                - Complete NCERT Curriculum (Classes 1-12)
                - 500+ Science Topics
                - Multi-language Support (10+ Indian Languages)
                - Real-time Progress Analytics
                - Advanced Gamification System
                - Mobile Responsive Design
                - WCAG 2.1 AA Accessibility
                
                🚀 **Performance:**
                - Supports 50+ Concurrent Users
                - Response Caching (40-60% Efficiency)
                - Database Connection Pooling
                - Async Operations
                
                🎨 **Premium UI/UX:**
                - Modern, Intuitive Interface
                - Dark/Light Theme Support
                - Smooth Animations
                - Professional Design
                
                Built with ❤️ in India 🇮🇳
                
                **Author:** Aseem Mehrotra  
                **Version:** 3.0.0  
                **License:** MIT
                """
            }
        )
    
    def load_custom_css(self) -> None:
        """Load premium custom CSS styling"""
        css_path = project_root / 'assets' / 'styles' / 'custom.css'
        
        if css_path.exists():
            try:
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
            except Exception as e:
                log_error(f"Failed to load custom CSS: {str(e)}")
    
    def initialize_session_state(self) -> None:
        """Initialize session state with default values"""
        defaults = {
            'user_id': None,
            'authenticated': False,
            'current_page': 'home',
            'theme': 'light',
            'language': 'English',
            'grade': 6,
            'subject': 'Physics',
            'points': 0,
            'streak': 0,
            'level': 'Beginner',
            'badges': [],
            'bookmarks': [],
            'preferences': {},
            'analytics_data': {},
            'current_topic': None,
            'quiz_state': {},
            'practice_history': [],
            'achievement_notifications': [],
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    async def initialize_database(self) -> bool:
        """Initialize database connection and schema"""
        try:
            if 'db_initialized' not in st.session_state:
                self.db_manager = DatabaseManager()
                await self.db_manager.initialize()
                st.session_state.db_initialized = True
                return True
            return True
        except Exception as e:
            handle_startup_error(f"Database initialization failed: {str(e)}")
            return False
    
    def validate_prerequisites(self) -> bool:
        """Validate application prerequisites"""
        try:
            # Check environment variables
            if not validate_environment():
                st.error("❌ Environment validation failed. Please check your configuration.")
                return False
            
            # Check required directories
            required_dirs = ['assets', 'backend', 'frontend', 'assets/styles']
            for dir_path in required_dirs:
                full_path = project_root / dir_path
                if not full_path.exists():
                    st.error(f"❌ Required directory missing: {dir_path}")
                    return False
            
            return True
        except Exception as e:
            handle_startup_error(f"Prerequisites validation failed: {str(e)}")
            return False
    
    def get_page_mapping(self) -> Dict[str, Any]:
        """Get mapping of page names to modules"""
        return {
            'home': home,
            'learn': learn,
            'practice': practice,
            'progress': progress,
            'achievements': achievements,
            'curriculum': curriculum_explorer,
            'settings': settings_page
        }
    
    def render_page(self, page_name: str) -> None:
        """Render the specified page"""
        pages = self.get_page_mapping()
        
        if page_name in pages:
            try:
                pages[page_name].render()
            except Exception as e:
                st.error(f"❌ Error rendering page '{page_name}': {str(e)}")
                log_error(f"Page render error - {page_name}: {str(e)}")
        else:
            st.error(f"❌ Page '{page_name}' not found")
    
    def render_layout(self) -> None:
        """Render the main application layout"""
        # Render header with branding
        render_header()
        
        # Main content area with navigation
        col1, col2 = st.columns([1, 4])
        
        with col1:
            # Render navigation sidebar
            selected_page = render_navigation()
            render_sidebar()
        
        with col2:
            # Render main content
            self.render_page(selected_page)
        
        # Render footer
        render_footer()
    
    async def run(self) -> None:
        """Main application run method"""
        # Configure Streamlit
        self.configure_streamlit()
        
        # Validate prerequisites
        if not self.validate_prerequisites():
            st.stop()
        
        # Initialize database
        if not await self.initialize_database():
            st.stop()
        
        # Load custom styling
        self.load_custom_css()
        
        # Initialize session state
        self.initialize_session_state()
        
        # Mark as initialized
        self.initialized = True
        
        # Render main layout
        self.render_layout()


def main():
    """Main entry point with error handling"""
    try:
        app = ScienceGPTApp()
        
        # Run the application (handling async)
        if hasattr(asyncio, 'run'):
            # Python 3.7+
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Already in an event loop, use create_task
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, app.run())
                        future.result()
                else:
                    asyncio.run(app.run())
            except RuntimeError:
                # Fallback for environments with existing event loops
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(app.run())
                finally:
                    loop.close()
        else:
            # Python 3.6 fallback
            loop = asyncio.get_event_loop()
            loop.run_until_complete(app.run())
    
    except Exception as e:
        handle_startup_error(f"Application startup failed: {str(e)}")


if __name__ == "__main__":
    main()
