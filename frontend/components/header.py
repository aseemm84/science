"""
Premium Header Component for ScienceGPT v3.0
Modern header with branding, user status, and quick actions
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any
import time

from backend.utils.analytics import track_user_activity


def render_header() -> None:
    """Render premium application header"""
    
    # Header CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -2rem 2rem -2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .header-content {
        position: relative;
        z-index: 2;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .header-stats {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.15);
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.2s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .stat-value {
        font-size: 1.4rem;
        font-weight: bold;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 0.2rem;
    }
    
    .header-actions {
        position: absolute;
        top: 1.5rem;
        right: 2rem;
        display: flex;
        gap: 1rem;
    }
    
    .action-btn {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .action-btn:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }
    
    .time-display {
        font-size: 0.9rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            margin: -1rem -1rem 2rem -1rem;
        }
        
        .header-title {
            font-size: 2rem;
        }
        
        .header-actions {
            position: relative;
            top: auto;
            right: auto;
            margin-top: 1rem;
            justify-content: center;
        }
        
        .header-stats {
            justify-content: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get user context
    user_id = st.session_state.get('user_id', 'guest')
    grade = st.session_state.get('grade', 6)
    subject = st.session_state.get('subject', 'Physics')
    points = st.session_state.get('points', 0)
    level = st.session_state.get('level', 'Beginner')
    streak = st.session_state.get('streak', 0)
    
    # Current date/time
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %B %d, %Y")
    
    # Greeting based on time
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning"
        greeting_icon = "🌅"
    elif hour < 17:
        greeting = "Good Afternoon"
        greeting_icon = "☀️"
    else:
        greeting = "Good Evening"
        greeting_icon = "🌙"
    
    # Header HTML
    header_html = f"""
    <div class="main-header">
        <div class="header-content">
            <div class="header-actions">
                <button class="action-btn" onclick="toggleNotifications()">
                    🔔 Notifications
                </button>
                <button class="action-btn" onclick="showProfile()">
                    👤 Profile
                </button>
            </div>
            
            <h1 class="header-title">
                🧪 ScienceGPT v3.0
                <span style="font-size: 1rem; font-weight: normal; opacity: 0.8;">
                    | World-Class AI Science Education
                </span>
            </h1>
            
            <p class="header-subtitle">
                {greeting_icon} {greeting}! Ready to explore the wonders of science today?
            </p>
            
            <div class="header-stats">
                <div class="stat-item">
                    <span class="stat-value">Grade {grade}</span>
                    <div class="stat-label">Current Level</div>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{subject}</span>
                    <div class="stat-label">Focus Subject</div>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{points}</span>
                    <div class="stat-label">Total Points</div>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{level}</span>
                    <div class="stat-label">Mastery Level</div>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{streak}</span>
                    <div class="stat-label">Day Streak</div>
                </div>
            </div>
            
            <div class="time-display">
                📅 {current_date} • ⏰ {current_time}
            </div>
        </div>
    </div>
    
    <script>
    function toggleNotifications() {{
        // This would integrate with Streamlit's notification system
        alert('Notifications feature - integrate with Streamlit state');
    }}
    
    function showProfile() {{
        // This would navigate to profile page
        alert('Profile page - integrate with Streamlit navigation');
    }}
    </script>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Track header interaction
    try:
        track_user_activity(
            user_id=user_id,
            activity_type='header_view',
            metadata={
                'time': current_time,
                'grade': grade,
                'subject': subject,
                'points': points
            }
        )
    except Exception:
        pass  # Silent fail for analytics


def render_welcome_banner() -> None:
    """Render welcome banner for new users"""
    
    if st.session_state.get('is_new_user', False):
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            animation: slideIn 0.5s ease-out;
        ">
            <h2 style="margin: 0 0 1rem 0; font-size: 2rem;">
                🎉 Welcome to ScienceGPT v3.0!
            </h2>
            <p style="margin: 0 0 1.5rem 0; font-size: 1.1rem; opacity: 0.9;">
                Your AI-powered journey to master science starts here. 
                Let's make learning fun, interactive, and effective!
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <span style="
                    background: rgba(255,255,255,0.2);
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">✨ AI-Powered Explanations</span>
                <span style="
                    background: rgba(255,255,255,0.2);
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">🎯 Personalized Learning</span>
                <span style="
                    background: rgba(255,255,255,0.2);
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                ">🏆 Gamified Progress</span>
            </div>
        </div>
        
        <style>
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Mark user as no longer new after showing banner
        st.session_state.is_new_user = False


def render_status_bar() -> None:
    """Render status bar with system information"""
    
    # System status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # AI Status
        ai_status = "🟢 Online" if st.session_state.get('ai_available', True) else "🔴 Offline"
        st.markdown(f"**AI Service:** {ai_status}")
    
    with col2:
        # Database Status
        db_status = "🟢 Connected" if st.session_state.get('db_connected', True) else "🔴 Disconnected"
        st.markdown(f"**Database:** {db_status}")
    
    with col3:
        # Cache Status
        cache_hit_rate = st.session_state.get('cache_hit_rate', 65)
        st.markdown(f"**Cache:** {cache_hit_rate}% hit rate")
    
    with col4:
        # Session Info
        session_time = st.session_state.get('session_start_time', time.time())
        minutes = int((time.time() - session_time) / 60)
        st.markdown(f"**Session:** {minutes} min")


def render_announcement_banner() -> None:
    """Render announcement banner for important updates"""
    
    announcements = st.session_state.get('announcements', [])
    
    for announcement in announcements:
        if not announcement.get('dismissed', False):
            
            color = {
                'info': '#3182ce',
                'success': '#38a169', 
                'warning': '#d69e2e',
                'error': '#e53e3e'
            }.get(announcement.get('type', 'info'), '#3182ce')
            
            st.markdown(f"""
            <div style="
                background: {color};
                color: white;
                padding: 1rem 2rem;
                margin: -1rem -2rem 2rem -2rem;
                text-align: center;
                font-weight: 500;
            ">
                📢 {announcement.get('message', 'Announcement')}
                <button style="
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    padding: 0.2rem 0.5rem;
                    border-radius: 10px;
                    margin-left: 1rem;
                    cursor: pointer;
                " onclick="dismissAnnouncement('{announcement.get('id', '')}')">
                    ✕
                </button>
            </div>
            """, unsafe_allow_html=True)
