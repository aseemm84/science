"""
Advanced Sidebar Component for ScienceGPT v3.0
Context-aware sidebar with user profile, settings, and quick tools
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional
import plotly.express as px
import plotly.graph_objects as go

from backend.curriculum.ncert_curriculum import get_curriculum, Subject
from backend.services.analytics_service import AnalyticsService
from frontend.widgets.charts import create_mini_progress_chart


def render_sidebar() -> None:
    """Render comprehensive sidebar with user context and tools"""
    
    # Current page context
    current_page = st.session_state.get('current_page', 'home')
    
    with st.sidebar:
        # User Profile Section
        render_user_profile()
        
        st.markdown("---")
        
        # Context-specific content based on current page
        if current_page == "learn":
            render_learning_sidebar()
        elif current_page == "practice":
            render_practice_sidebar()
        elif current_page == "curriculum":
            render_curriculum_sidebar()
        elif current_page == "progress":
            render_progress_sidebar()
        elif current_page == "achievements":
            render_achievements_sidebar()
        else:
            render_home_sidebar()
        
        st.markdown("---")
        
        # Common tools
        render_common_tools()
        
        st.markdown("---")
        
        # Settings and help
        render_sidebar_footer()


def render_user_profile() -> None:
    """Render user profile section in sidebar"""
    
    st.markdown("### 👤 Your Profile")
    
    # User basic info
    grade = st.session_state.get('grade', 6)
    subject = st.session_state.get('subject', 'Physics')
    points = st.session_state.get('points', 0)
    level = st.session_state.get('level', 'Beginner')
    
    # Profile card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎓</div>
        <div style="font-weight: bold; font-size: 1.1rem;">Grade {grade} Student</div>
        <div style="opacity: 0.8; margin: 0.3rem 0;">{subject} • {level}</div>
        <div style="
            background: rgba(255,255,255,0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            display: inline-block;
            margin-top: 0.5rem;
            font-weight: bold;
        ">
            ✨ {points} Points
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2 = st.columns(2)
    
    with col1:
        streak = st.session_state.get('streak', 0)
        st.metric("🔥 Streak", f"{streak} days")
    
    with col2:
        badges = len(st.session_state.get('badges', []))
        st.metric("🏆 Badges", badges)


def render_learning_sidebar() -> None:
    """Render learning-specific sidebar content"""
    
    st.markdown("### 🧠 Learning Tools")
    
    # Subject selector
    current_subject = st.selectbox(
        "📚 Subject",
        ["Physics", "Chemistry", "Biology"],
        index=["Physics", "Chemistry", "Biology"].index(st.session_state.get('subject', 'Physics'))
    )
    
    if current_subject != st.session_state.get('subject'):
        st.session_state.subject = current_subject
        st.rerun()
    
    # Grade selector
    current_grade = st.selectbox(
        "🎓 Grade",
        list(range(1, 13)),
        index=st.session_state.get('grade', 6) - 1
    )
    
    if current_grade != st.session_state.get('grade'):
        st.session_state.grade = current_grade
        st.rerun()
    
    # Language preference
    languages = ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati"]
    current_language = st.selectbox(
        "🗣️ Language",
        languages,
        index=languages.index(st.session_state.get('language', 'English'))
    )
    
    if current_language != st.session_state.get('language'):
        st.session_state.language = current_language
        st.rerun()
    
    st.markdown("### 💡 Quick Questions")
    
    # Suggested questions based on current context
    curriculum = get_curriculum()
    subject_enum = Subject.PHYSICS if current_subject == "Physics" else (
        Subject.CHEMISTRY if current_subject == "Chemistry" else Subject.BIOLOGY
    )
    
    topics = curriculum.get_topics_by_grade_subject(current_grade, subject_enum)
    
    if topics:
        st.markdown("**Recent topics:**")
        for topic in topics[:5]:
            if st.button(f"📖 {topic.title}", key=f"topic_btn_{topic.id}"):
                st.session_state.suggested_question = f"Explain {topic.title}"
                st.rerun()
    
    # Study tips
    st.markdown("### 📝 Study Tips")
    
    tips = [
        "🎯 Set clear learning goals for each session",
        "⏰ Take breaks every 25 minutes",
        "🔄 Review previous topics regularly",
        "❓ Ask questions when confused",
        "🏆 Celebrate small wins"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")


def render_practice_sidebar() -> None:
    """Render practice-specific sidebar content"""
    
    st.markdown("### 📝 Practice Options")
    
    # Quiz preferences
    st.markdown("**Quiz Settings:**")
    
    difficulty = st.radio(
        "Difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        index=1
    )
    
    num_questions = st.slider(
        "Number of Questions",
        min_value=5,
        max_value=20,
        value=10
    )
    
    time_limit = st.checkbox("Enable Time Limit", value=True)
    
    if time_limit:
        minutes = st.slider("Time Limit (minutes)", 5, 30, 15)
    
    # Subject focus
    st.markdown("**Subject Focus:**")
    
    subject_weights = {}
    for subject in ["Physics", "Chemistry", "Biology"]:
        weight = st.slider(
            f"{subject} %",
            0, 100, 33,
            key=f"weight_{subject.lower()}"
        )
        subject_weights[subject] = weight
    
    # Recent quiz performance
    st.markdown("### 📊 Recent Performance")
    
    quiz_history = st.session_state.get('quiz_history', [])
    
    if quiz_history:
        # Create mini chart of recent scores
        recent_scores = [q.get('score', 0) for q in quiz_history[-10:]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=recent_scores,
            mode='lines+markers',
            line=dict(color='#667eea', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            height=150,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        avg_score = sum(recent_scores) / len(recent_scores)
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    else:
        st.info("Take your first quiz to see performance metrics!")


def render_curriculum_sidebar() -> None:
    """Render curriculum explorer sidebar"""
    
    st.markdown("### 📚 Curriculum Navigator")
    
    # Grade and subject filters
    grade_range = st.slider(
        "Grade Range",
        1, 12, (6, 10),
        help="Select range of grades to explore"
    )
    
    subject_filter = st.multiselect(
        "Subjects",
        ["Physics", "Chemistry", "Biology"],
        default=["Physics", "Chemistry", "Biology"]
    )
    
    # Difficulty filter
    difficulty_filter = st.multiselect(
        "Difficulty Levels",
        ["Beginner", "Intermediate", "Advanced"],
        default=["Beginner", "Intermediate", "Advanced"]
    )
    
    # Search within curriculum
    st.markdown("### 🔍 Search Topics")
    
    search_query = st.text_input(
        "Search topics...",
        placeholder="e.g., photosynthesis, electricity"
    )
    
    if search_query:
        curriculum = get_curriculum()
        results = curriculum.search_topics(search_query)
        
        st.markdown(f"**Found {len(results)} topics:**")
        
        for result in results[:10]:
            with st.expander(f"📖 {result.title} (Grade {result.grade})"):
                st.markdown(f"**Subject:** {result.subject.value}")
                st.markdown(f"**Description:** {result.description}")
                st.markdown(f"**Keywords:** {', '.join(result.keywords[:5])}")
    
    # Curriculum statistics
    st.markdown("### 📊 Curriculum Stats")
    
    curriculum = get_curriculum()
    stats = curriculum.get_curriculum_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Topics", stats["total_topics"])
    
    with col2:
        st.metric("Grades", len(stats["grades_covered"]))


def render_progress_sidebar() -> None:
    """Render progress analytics sidebar"""
    
    st.markdown("### 📊 Analytics Tools")
    
    # Time period selector
    time_period = st.selectbox(
        "Time Period",
        ["Last 7 days", "Last 30 days", "Last 3 months", "All time"],
        index=1
    )
    
    # Metrics to display
    metrics = st.multiselect(
        "Show Metrics",
        ["Points", "Quiz Scores", "Study Time", "Topics Covered", "Streaks"],
        default=["Points", "Quiz Scores"]
    )
    
    # Subject breakdown
    st.markdown("### 📚 Subject Progress")
    
    mastery_levels = st.session_state.get('mastery_levels', {})
    
    for subject, points in mastery_levels.items():
        progress = min(100, (points / 100) * 100)  # Assume 100 points = 100%
        
        st.markdown(f"**{subject}**")
        st.progress(progress / 100)
        st.caption(f"{points} points • {progress:.0f}% mastery")
    
    # Learning goals
    st.markdown("### 🎯 Learning Goals")
    
    goals = st.session_state.get('learning_goals', [])
    
    if not goals:
        if st.button("Set Learning Goals"):
            st.session_state.show_goals_modal = True
            st.rerun()
    else:
        for goal in goals:
            progress = goal.get('progress', 0)
            st.markdown(f"**{goal.get('title', 'Goal')}**")
            st.progress(progress / 100)
            st.caption(f"{progress}% complete")


def render_achievements_sidebar() -> None:
    """Render achievements sidebar"""
    
    st.markdown("### 🏆 Badge Categories")
    
    categories = ["Learning", "Quizzes", "Streaks", "Exploration", "Special"]
    
    selected_category = st.radio(
        "Filter by category:",
        categories
    )
    
    # Achievement progress
    st.markdown("### 📈 Progress to Next Badge")
    
    # Example achievements progress
    achievements_progress = [
        {"name": "Quiz Master", "progress": 75, "target": "Complete 20 quizzes"},
        {"name": "Streak Keeper", "progress": 60, "target": "Maintain 14-day streak"},
        {"name": "Explorer", "progress": 30, "target": "Study 50 topics"}
    ]
    
    for achievement in achievements_progress:
        st.markdown(f"**{achievement['name']}**")
        st.progress(achievement['progress'] / 100)
        st.caption(achievement['target'])
    
    # Badge showcase
    st.markdown("### ✨ Recent Badges")
    
    badges = st.session_state.get('badges', [])
    
    if badges:
        for badge in badges[-3:]:  # Show last 3 badges
            st.markdown(f"🏅 **{badge.get('name', 'Badge')}**")
            st.caption(badge.get('description', 'Achievement unlocked!'))
    else:
        st.info("Earn your first badge by completing activities!")


def render_home_sidebar() -> None:
    """Render home dashboard sidebar"""
    
    st.markdown("### 🎯 Today's Focus")
    
    # Daily goals
    daily_goals = [
        {"task": "Ask 3 questions", "progress": 2, "target": 3},
        {"task": "Complete 1 quiz", "progress": 0, "target": 1},
        {"task": "Study for 30 min", "progress": 15, "target": 30}
    ]
    
    for goal in daily_goals:
        progress_pct = (goal['progress'] / goal['target']) * 100
        
        st.markdown(f"**{goal['task']}**")
        st.progress(min(1.0, progress_pct / 100))
        st.caption(f"{goal['progress']}/{goal['target']}")
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        questions_today = st.session_state.get('questions_today', 0)
        st.metric("Questions Today", questions_today)
    
    with col2:
        time_spent = st.session_state.get('time_spent_today', 0)
        st.metric("Time Spent", f"{time_spent} min")
    
    # Motivational message
    st.markdown("### 💪 Stay Motivated!")
    
    motivational_messages = [
        "🌟 Every question brings you closer to mastery!",
        "🚀 Consistent learning leads to great achievements!",
        "🎓 Knowledge is the best investment!",
        "💡 Curiosity is the engine of learning!",
        "🏆 Small progress daily = big results yearly!"
    ]
    
    import random
    message = random.choice(motivational_messages)
    
    st.info(message)


def render_common_tools() -> None:
    """Render common tools available across all pages"""
    
    st.markdown("### ⚡ Quick Tools")
    
    # Theme toggle
    if st.button("🎨 Toggle Theme", use_container_width=True):
        current_theme = st.session_state.get('theme', 'light')
        st.session_state.theme = 'dark' if current_theme == 'light' else 'light'
        st.rerun()
    
    # Audio toggle
    audio_enabled = st.session_state.get('audio_enabled', True)
    if st.button(
        "🔊 Audio ON" if audio_enabled else "🔇 Audio OFF",
        use_container_width=True
    ):
        st.session_state.audio_enabled = not audio_enabled
        st.rerun()
    
    # Export progress
    if st.button("📤 Export Progress", use_container_width=True):
        st.session_state.show_export_modal = True
        st.rerun()


def render_sidebar_footer() -> None:
    """Render sidebar footer with settings and help"""
    
    st.markdown("### ⚙️ Settings & Help")
    
    # Quick settings
    if st.button("🛠️ Full Settings", use_container_width=True):
        st.session_state.current_page = "settings"
        st.rerun()
    
    if st.button("❓ Help & Support", use_container_width=True):
        st.session_state.show_help_modal = True
        st.rerun()
    
    # App info
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; opacity: 0.6; font-size: 0.8rem;">
        <strong>ScienceGPT v3.0</strong><br>
        Built with ❤️ in India<br>
        <em>Making science education accessible</em>
    </div>
    """, unsafe_allow_html=True)


def render_notification_center() -> None:
    """Render notification center in sidebar"""
    
    notifications = st.session_state.get('notifications', [])
    
    if notifications:
        st.markdown("### 🔔 Notifications")
        
        for notification in notifications[-5:]:  # Show last 5
            notification_type = notification.get('type', 'info')
            
            if notification_type == 'achievement':
                st.success(f"🏆 {notification['message']}")
            elif notification_type == 'reminder':
                st.info(f"⏰ {notification['message']}")
            elif notification_type == 'tip':
                st.info(f"💡 {notification['message']}")
            else:
                st.info(notification['message'])
        
        if st.button("Clear Notifications"):
            st.session_state.notifications = []
            st.rerun()
