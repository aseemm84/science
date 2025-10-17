"""
Home Dashboard Page for ScienceGPT v3.0
Overview dashboard with stats, recent activity, and quick actions
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any

from frontend.components.navigation import render_page_header, render_breadcrumb
from frontend.widgets.cards import render_stat_card, render_activity_card, render_quick_action_card
from frontend.widgets.charts import create_progress_chart, create_performance_trend_chart
from backend.services.analytics_service import AnalyticsService
from backend.services.recommendation_engine import RecommendationEngine


def render() -> None:
    """Render home dashboard page"""
    
    # Page header
    render_page_header(
        title="Dashboard",
        description="Welcome back! Here's your learning overview.",
        icon="🏠"
    )
    
    # Breadcrumb navigation
    render_breadcrumb("home")
    
    # Main dashboard content
    render_dashboard_overview()
    
    st.markdown("---")
    
    # Dashboard sections
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_recent_activity()
        render_learning_progress()
    
    with col2:
        render_quick_stats()
        render_daily_goals()
        render_recommendations()


def render_dashboard_overview() -> None:
    """Render dashboard overview with key metrics"""
    
    st.markdown("### 📊 Today's Overview")
    
    # Get user stats
    total_points = st.session_state.get('points', 0)
    questions_today = st.session_state.get('questions_today', 0)
    time_spent_today = st.session_state.get('time_spent_today', 0)
    streak = st.session_state.get('streak', 0)
    level = st.session_state.get('level', 'Beginner')
    
    # Overview cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_stat_card(
            title="Total Points",
            value=total_points,
            icon="✨",
            color="#4facfe",
            trend="+12 today"
        )
    
    with col2:
        render_stat_card(
            title="Questions Asked",
            value=questions_today,
            icon="❓",
            color="#667eea",
            trend="Keep going!"
        )
    
    with col3:
        render_stat_card(
            title="Study Time",
            value=f"{time_spent_today}m",
            icon="⏱️",
            color="#764ba2",
            trend="Goal: 30m"
        )
    
    with col4:
        render_stat_card(
            title="Current Streak",
            value=f"{streak} days",
            icon="🔥",
            color="#f093fb",
            trend="Keep it up!"
        )
    
    with col5:
        render_stat_card(
            title="Current Level",
            value=level,
            icon="🎓",
            color="#4facfe",
            trend="Growing!"
        )


def render_recent_activity() -> None:
    """Render recent learning activity"""
    
    st.markdown("### 🕒 Recent Activity")
    
    # Sample recent activities
    recent_activities = [
        {
            "type": "question",
            "title": "Asked about Photosynthesis",
            "subject": "Biology",
            "time": "2 minutes ago",
            "icon": "❓",
            "color": "#4CAF50"
        },
        {
            "type": "quiz",
            "title": "Completed Physics Quiz - Motion",
            "subject": "Physics", 
            "score": 85,
            "time": "15 minutes ago",
            "icon": "📝",
            "color": "#2196F3"
        },
        {
            "type": "achievement",
            "title": "Earned 'Curious Mind' Badge",
            "description": "Asked 10 questions",
            "time": "1 hour ago",
            "icon": "🏆",
            "color": "#FF9800"
        },
        {
            "type": "study",
            "title": "Studied Chemical Reactions",
            "subject": "Chemistry",
            "duration": "25 minutes",
            "time": "2 hours ago",
            "icon": "📚",
            "color": "#9C27B0"
        }
    ]
    
    for activity in recent_activities:
        render_activity_card(activity)


def render_learning_progress() -> None:
    """Render learning progress charts"""
    
    st.markdown("### 📈 Learning Progress")
    
    # Progress tabs
    tab1, tab2, tab3 = st.tabs(["📊 Subject Progress", "📅 Weekly Activity", "🎯 Goals"])
    
    with tab1:
        # Subject mastery progress
        mastery_data = {
            "Physics": st.session_state.get('mastery_levels', {}).get('Physics', 25),
            "Chemistry": st.session_state.get('mastery_levels', {}).get('Chemistry', 35),
            "Biology": st.session_state.get('mastery_levels', {}).get('Biology', 42)
        }
        
        fig = create_progress_chart(mastery_data)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Weekly activity chart
        dates = [(datetime.now() - timedelta(days=i)).strftime("%a") for i in range(7)][::-1]
        activity_data = [12, 8, 15, 10, 20, 5, 8]  # Sample data
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=activity_data,
            marker_color='#4facfe',
            name="Questions Asked"
        ))
        
        fig.update_layout(
            title="Questions Asked This Week",
            height=300,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Daily goals progress
        goals = [
            {"name": "Ask 5 Questions", "current": 3, "target": 5, "icon": "❓"},
            {"name": "Complete 1 Quiz", "current": 1, "target": 1, "icon": "📝"},
            {"name": "Study 30 Minutes", "current": 22, "target": 30, "icon": "⏱️"}
        ]
        
        for goal in goals:
            progress = (goal['current'] / goal['target']) * 100
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{goal['icon']} {goal['name']}**")
                st.progress(min(1.0, progress / 100))
                st.caption(f"{goal['current']}/{goal['target']} completed")
            
            with col2:
                if progress >= 100:
                    st.success("✅ Done!")
                else:
                    remaining = goal['target'] - goal['current']
                    st.info(f"{remaining} more")


def render_quick_stats() -> None:
    """Render quick statistics sidebar"""
    
    st.markdown("### ⚡ Quick Stats")
    
    # This week vs last week comparison
    stats_comparison = [
        {
            "metric": "Points Earned",
            "current": 156,
            "previous": 142,
            "icon": "✨"
        },
        {
            "metric": "Time Studied",
            "current": 180,  # minutes
            "previous": 165,
            "icon": "⏱️",
            "unit": "min"
        },
        {
            "metric": "Topics Covered",
            "current": 8,
            "previous": 6,
            "icon": "📚"
        },
        {
            "metric": "Quiz Average",
            "current": 78.5,
            "previous": 75.2,
            "icon": "📊",
            "unit": "%"
        }
    ]
    
    for stat in stats_comparison:
        change = stat['current'] - stat['previous']
        change_pct = (change / stat['previous']) * 100 if stat['previous'] > 0 else 0
        
        unit = stat.get('unit', '')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.metric(
                f"{stat['icon']} {stat['metric']}", 
                f"{stat['current']}{unit}",
                f"{change:+.1f}{unit} ({change_pct:+.1f}%)"
            )
        
        with col2:
            if change > 0:
                st.success("↗️")
            elif change < 0:
                st.error("↘️")
            else:
                st.info("→")


def render_daily_goals() -> None:
    """Render daily goals section"""
    
    st.markdown("### 🎯 Today's Goals")
    
    # Daily challenge
    st.markdown("#### 🔥 Daily Challenge")
    
    challenge = {
        "title": "Chemistry Explorer",
        "description": "Learn about 3 chemical reactions",
        "progress": 1,
        "target": 3,
        "reward": "50 points + Special Badge",
        "time_left": "18 hours left"
    }
    
    progress_pct = (challenge['progress'] / challenge['target']) * 100
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    ">
        <div style="font-weight: bold; margin-bottom: 0.5rem;">{challenge['title']}</div>
        <div style="opacity: 0.9; margin-bottom: 0.8rem;">{challenge['description']}</div>
        <div style="background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; margin-bottom: 0.5rem;">
            <div style="background: white; height: 100%; width: {progress_pct}%; border-radius: 4px;"></div>
        </div>
        <div style="font-size: 0.9rem; opacity: 0.8;">
            {challenge['progress']}/{challenge['target']} • {challenge['reward']} • ⏰ {challenge['time_left']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Challenge", use_container_width=True, type="primary"):
        st.session_state.current_page = "learn"
        st.session_state.challenge_active = True
        st.rerun()


def render_recommendations() -> None:
    """Render personalized recommendations"""
    
    st.markdown("### 💡 Recommended for You")
    
    try:
        # Get recommendations from service
        rec_engine = RecommendationEngine()
        user_context = {
            'grade': st.session_state.get('grade', 6),
            'subject': st.session_state.get('subject', 'Physics'),
            'recent_topics': st.session_state.get('recent_topics', []),
            'weak_areas': st.session_state.get('weak_areas', [])
        }
        
        recommendations = rec_engine.get_personalized_recommendations(
            st.session_state.get('user_id', 'guest'),
            user_context
        )
        
    except Exception:
        # Fallback recommendations
        recommendations = [
            {
                "type": "topic",
                "title": "Chemical Bonding Basics",
                "description": "Perfect next step after atomic structure",
                "subject": "Chemistry",
                "grade": st.session_state.get('grade', 10),
                "confidence": 0.85
            },
            {
                "type": "quiz", 
                "title": "Motion and Forces Quiz",
                "description": "Test your physics knowledge",
                "subject": "Physics",
                "grade": st.session_state.get('grade', 10),
                "confidence": 0.78
            },
            {
                "type": "review",
                "title": "Photosynthesis Review",
                "description": "Revisit this important topic",
                "subject": "Biology", 
                "grade": st.session_state.get('grade', 10),
                "confidence": 0.72
            }
        ]
    
    for rec in recommendations[:3]:
        confidence_color = "#4CAF50" if rec['confidence'] > 0.8 else "#FF9800" if rec['confidence'] > 0.7 else "#f44336"
        
        st.markdown(f"""
        <div style="
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            background: white;
        ">
            <div style="font-weight: bold; color: #2d3748; margin-bottom: 0.3rem;">
                {'📖' if rec['type'] == 'topic' else '📝' if rec['type'] == 'quiz' else '🔄'} {rec['title']}
            </div>
            <div style="color: #4a5568; font-size: 0.9rem; margin-bottom: 0.5rem;">
                {rec['description']}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="
                    background: rgba(102, 126, 234, 0.1);
                    color: #667eea;
                    padding: 0.2rem 0.5rem;
                    border-radius: 12px;
                    font-size: 0.8rem;
                ">
                    {rec['subject']} • Grade {rec['grade']}
                </span>
                <span style="color: {confidence_color}; font-size: 0.8rem; font-weight: bold;">
                    {rec['confidence']*100:.0f}% match
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🎯 Get More Recommendations", use_container_width=True):
        st.session_state.current_page = "progress"
        st.rerun()


def render_quick_actions() -> None:
    """Render quick action buttons"""
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧠 Continue Learning", use_container_width=True, type="primary"):
            st.session_state.current_page = "learn"
            st.rerun()
        
        if st.button("📝 Take Random Quiz", use_container_width=True):
            st.session_state.current_page = "practice"
            st.session_state.quick_action = "random_quiz"
            st.rerun()
    
    with col2:
        if st.button("📚 Browse Topics", use_container_width=True):
            st.session_state.current_page = "curriculum"
            st.rerun()
        
        if st.button("📊 View Progress", use_container_width=True):
            st.session_state.current_page = "progress"
            st.rerun()


def render_achievement_showcase() -> None:
    """Render recent achievements showcase"""
    
    st.markdown("### 🏆 Recent Achievements")
    
    recent_badges = st.session_state.get('badges', [])
    
    if recent_badges:
        for badge in recent_badges[-3:]:  # Show last 3 badges
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 1rem;
                border-radius: 12px;
                margin-bottom: 0.5rem;
            ">
                <div style="font-size: 2rem; margin-right: 1rem;">🏅</div>
                <div>
                    <div style="font-weight: bold;">{badge.get('name', 'Achievement')}</div>
                    <div style="opacity: 0.8; font-size: 0.9rem;">{badge.get('description', 'Well done!')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎯 Complete activities to earn your first achievement!")
