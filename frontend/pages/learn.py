"""
Interactive Learning Page for ScienceGPT v3.0
AI-powered question and answer interface with context awareness
"""

import streamlit as st
import asyncio
import time
from typing import Dict, Any, Optional

from frontend.components.navigation import render_page_header, render_breadcrumb
from frontend.widgets.cards import render_ai_response_card
from backend.ai.llm_handler import LLMHandler
from backend.curriculum.ncert_curriculum import get_curriculum, Subject
from backend.services.analytics_service import AnalyticsService


def render() -> None:
    """Render interactive learning page"""
    
    # Page header
    render_page_header(
        title="Interactive Learning",
        description="Ask questions and get AI-powered explanations tailored to your grade and subject.",
        icon="🧠"
    )
    
    # Breadcrumb
    render_breadcrumb("learn")
    
    # Main learning interface
    render_learning_interface()
    
    # Learning tools sidebar
    render_learning_tools()


def render_learning_interface() -> None:
    """Render main learning question/answer interface"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Question input section
        render_question_input()
        
        # Conversation history
        render_conversation_history()
    
    with col2:
        # Context panel
        render_context_panel()
        
        # Suggested questions
        render_suggested_questions()


def render_question_input() -> None:
    """Render question input interface"""
    
    st.markdown("### ❓ Ask Your Science Question")
    
    # Pre-fill if suggested question exists
    suggested_question = st.session_state.get('suggested_question', '')
    
    # Question input
    with st.form("question_form", clear_on_submit=True):
        question = st.text_area(
            "What would you like to learn about?",
            value=suggested_question,
            height=100,
            placeholder="e.g., How does photosynthesis work? What is Newton's first law? Why do atoms bond?",
            help="Ask any science question related to your current grade and subject."
        )
        
        # Input options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_examples = st.checkbox("Include Indian examples", value=True)
        
        with col2:
            detailed_explanation = st.checkbox("Detailed explanation", value=False)
        
        with col3:
            voice_response = st.checkbox("Voice response", value=False)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Get AI Explanation", use_container_width=True, type="primary")
        
        if submitted and question.strip():
            # Clear suggested question
            if 'suggested_question' in st.session_state:
                del st.session_state.suggested_question
            
            # Process question
            process_question(
                question=question,
                include_examples=include_examples,
                detailed=detailed_explanation,
                voice=voice_response
            )


def process_question(question: str, include_examples: bool = True, detailed: bool = False, voice: bool = False) -> None:
    """Process user question and generate AI response"""
    
    # Show processing indicator
    with st.spinner("🤖 AI is thinking..."):
        
        # Get user context
        grade = st.session_state.get('grade', 6)
        subject = st.session_state.get('subject', 'Physics')
        language = st.session_state.get('language', 'English')
        
        # Build context for AI
        context = {
            "type": "concept_explanation",
            "grade": grade,
            "subject": subject,
            "language": language,
            "include_examples": include_examples,
            "detailed": detailed,
            "curriculum": "NCERT"
        }
        
        try:
            # Get AI response
            llm_handler = LLMHandler()
            
            # Use asyncio to handle the async call
            response = asyncio.run(
                llm_handler.explain_concept(
                    topic=question,
                    grade=grade,
                    subject=subject,
                    language=language,
                    include_examples=include_examples
                )
            )
            
            # Store conversation
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = []
            
            conversation_entry = {
                'timestamp': time.time(),
                'question': question,
                'response': response.content,
                'context': context,
                'metadata': {
                    'provider': response.provider.value,
                    'model': response.model,
                    'tokens_used': response.tokens_used,
                    'response_time_ms': response.response_time_ms,
                    'cached': response.cached
                }
            }
            
            st.session_state.conversation_history.append(conversation_entry)
            
            # Update user stats
            st.session_state.questions_today = st.session_state.get('questions_today', 0) + 1
            st.session_state.points = st.session_state.get('points', 0) + 5  # 5 points per question
            
            # Track analytics
            try:
                analytics = AnalyticsService()
                analytics.track_learning_activity(
                    user_id=st.session_state.get('user_id', 'guest'),
                    activity_type='question_asked',
                    subject=subject,
                    grade=grade,
                    metadata={
                        'question_length': len(question),
                        'response_time_ms': response.response_time_ms,
                        'cached': response.cached
                    }
                )
            except Exception:
                pass  # Silent fail for analytics
            
            st.success("✅ Answer generated successfully!")
            
            # Show points earned
            st.balloons()
            st.info(f"🎉 You earned 5 points! Total: {st.session_state.get('points', 0)}")
            
            # Voice response if requested
            if voice and response.content:
                try:
                    # This would integrate with TTS service
                    st.audio("placeholder.mp3")  # Placeholder
                except Exception:
                    st.warning("Voice response not available at the moment.")
            
        except Exception as e:
            st.error(f"❌ Sorry, I couldn't process your question: {str(e)}")
            st.info("💡 Try rephrasing your question or check your internet connection.")


def render_conversation_history() -> None:
    """Render conversation history"""
    
    conversation_history = st.session_state.get('conversation_history', [])
    
    if not conversation_history:
        st.markdown("### 💬 Conversation History")
        st.info("🚀 Ask your first question to start learning!")
        return
    
    st.markdown("### 💬 Your Learning Conversation")
    
    # Reverse to show latest first
    for i, entry in enumerate(reversed(conversation_history[-10:])):  # Show last 10
        
        timestamp = time.strftime("%H:%M", time.localtime(entry['timestamp']))
        
        with st.expander(f"🕐 {timestamp} - {entry['question'][:50]}..."):
            
            # Question
            st.markdown(f"**❓ Your Question:**")
            st.markdown(f"*{entry['question']}*")
            
            # Response
            st.markdown(f"**🤖 AI Response:**")
            render_ai_response_card(entry['response'])
            
            # Metadata
            with st.expander("ℹ️ Response Details"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("AI Provider", entry['metadata'].get('provider', 'Unknown'))
                
                with col2:
                    st.metric("Response Time", f"{entry['metadata'].get('response_time_ms', 0)}ms")
                
                with col3:
                    cached_status = "Yes" if entry['metadata'].get('cached', False) else "No"
                    st.metric("Cached", cached_status)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔖 Bookmark", key=f"bookmark_{i}"):
                    # Add to bookmarks
                    bookmark_entry(entry)
                    st.success("Added to bookmarks!")
            
            with col2:
                if st.button("🔄 Ask Follow-up", key=f"followup_{i}"):
                    st.session_state.suggested_question = f"Can you explain more about {entry['question'][:30]}...?"
                    st.rerun()
            
            with col3:
                if st.button("📤 Share", key=f"share_{i}"):
                    # Generate shareable link or content
                    st.info("Sharing feature coming soon!")


def render_context_panel() -> None:
    """Render learning context and settings panel"""
    
    st.markdown("### 📚 Learning Context")
    
    # Current settings
    grade = st.session_state.get('grade', 6)
    subject = st.session_state.get('subject', 'Physics')
    language = st.session_state.get('language', 'English')
    
    st.info(f"**Grade:** {grade} | **Subject:** {subject} | **Language:** {language}")
    
    # Quick settings adjustment
    with st.expander("⚙️ Adjust Learning Settings"):
        
        new_grade = st.selectbox(
            "Grade Level",
            range(1, 13),
            index=grade-1,
            key="learn_grade"
        )
        
        new_subject = st.selectbox(
            "Subject Focus",
            ["Physics", "Chemistry", "Biology"],
            index=["Physics", "Chemistry", "Biology"].index(subject),
            key="learn_subject"
        )
        
        new_language = st.selectbox(
            "Explanation Language",
            ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi"],
            index=0 if language not in ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi"] else ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi"].index(language),
            key="learn_language"
        )
        
        if st.button("✅ Update Settings"):
            st.session_state.grade = new_grade
            st.session_state.subject = new_subject
            st.session_state.language = new_language
            st.success("Settings updated!")
            st.rerun()
    
    # Learning progress for current session
    st.markdown("### 📊 Session Progress")
    
    questions_today = st.session_state.get('questions_today', 0)
    points_today = questions_today * 5  # Assuming 5 points per question
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Questions Asked", questions_today)
    
    with col2:
        st.metric("Points Earned", points_today)
    
    # Daily goal progress
    daily_goal = 5  # questions per day
    progress = min(1.0, questions_today / daily_goal)
    
    st.markdown("**Daily Goal Progress:**")
    st.progress(progress)
    st.caption(f"{questions_today}/{daily_goal} questions today")
    
    if progress >= 1.0:
        st.success("🎉 Daily goal achieved!")


def render_suggested_questions() -> None:
    """Render AI-generated suggested questions"""
    
    st.markdown("### 💡 Suggested Questions")
    
    grade = st.session_state.get('grade', 6)
    subject = st.session_state.get('subject', 'Physics')
    
    # Try to get curriculum-based suggestions
    try:
        curriculum = get_curriculum()
        subject_enum = Subject.PHYSICS if subject == "Physics" else (
            Subject.CHEMISTRY if subject == "Chemistry" else Subject.BIOLOGY
        )
        
        topics = curriculum.get_topics_by_grade_subject(grade, subject_enum)
        
        suggested_questions = []
        
        for topic in topics[:5]:  # Get first 5 topics
            questions = [
                f"What is {topic.title}?",
                f"How does {topic.title} work?",
                f"Why is {topic.title} important?",
                f"Give me examples of {topic.title}"
            ]
            suggested_questions.extend(questions)
        
        # Limit to 8 suggestions
        suggested_questions = suggested_questions[:8]
        
    except Exception:
        # Fallback suggestions
        suggested_questions = [
            f"What are the basic concepts in Grade {grade} {subject}?",
            f"How do I prepare for {subject} exams?",
            f"What are some real-world applications of {subject}?",
            f"What are the most important topics in {subject}?",
            f"How can I improve my understanding of {subject}?",
            f"What experiments can I do to learn {subject}?",
            f"What are common mistakes in {subject}?",
            f"How is {subject} used in daily life in India?"
        ]
    
    for i, question in enumerate(suggested_questions):
        if st.button(f"💭 {question}", key=f"suggested_{i}"):
            st.session_state.suggested_question = question
            st.rerun()


def render_learning_tools() -> None:
    """Render additional learning tools"""
    
    st.markdown("---")
    st.markdown("### 🛠️ Learning Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Virtual Lab", use_container_width=True):
            st.info("Virtual experiments coming soon!")
        
        if st.button("📖 Study Notes", use_container_width=True):
            st.session_state.current_page = "curriculum"
            st.rerun()
    
    with col2:
        if st.button("🎥 Video Lessons", use_container_width=True):
            st.info("Video content coming soon!")
        
        if st.button("🤝 Study Groups", use_container_width=True):
            st.info("Collaborative learning coming soon!")


def bookmark_entry(entry: Dict[str, Any]) -> None:
    """Add conversation entry to bookmarks"""
    
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
    
    bookmark = {
        'id': len(st.session_state.bookmarks) + 1,
        'timestamp': entry['timestamp'],
        'question': entry['question'],
        'answer': entry['response'],
        'subject': entry['context'].get('subject', 'Science'),
        'grade': entry['context'].get('grade', 6),
        'tags': [],
        'notes': ''
    }
    
    st.session_state.bookmarks.append(bookmark)
    
    # Award points for bookmarking
    st.session_state.points = st.session_state.get('points', 0) + 2
