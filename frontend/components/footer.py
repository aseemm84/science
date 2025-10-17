"""
Premium Footer Component for ScienceGPT v3.0
Modern footer with links, social media, and app information
"""

import streamlit as st
from datetime import datetime


def render_footer() -> None:
    """Render premium application footer"""
    
    # Footer CSS
    st.markdown("""
    <style>
    .main-footer {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 3rem 2rem 2rem 2rem;
        margin: 3rem -2rem -2rem -2rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-section h3 {
        color: #4facfe;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .footer-section a {
        color: #e2e8f0;
        text-decoration: none;
        display: block;
        margin-bottom: 0.5rem;
        transition: color 0.3s ease;
    }
    
    .footer-section a:hover {
        color: #4facfe;
    }
    
    .footer-bottom {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1.5rem;
        text-align: center;
        opacity: 0.8;
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .social-link {
        background: rgba(74, 172, 254, 0.2);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .social-link:hover {
        background: #4facfe;
        transform: translateY(-2px);
    }
    
    @media (max-width: 768px) {
        .main-footer {
            margin: 3rem -1rem -2rem -1rem;
            padding: 2rem 1rem 1.5rem 1rem;
        }
        
        .footer-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    current_year = datetime.now().year
    
    footer_html = f"""
    <div class="main-footer">
        <div class="footer-content">
            <div class="footer-grid">
                <div class="footer-section">
                    <h3>🧪 ScienceGPT v3.0</h3>
                    <p style="margin-bottom: 1rem; opacity: 0.9; line-height: 1.6;">
                        World-class AI-powered science education platform designed specifically 
                        for Indian students. Making science learning accessible, engaging, and effective.
                    </p>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        <span style="background: rgba(74, 172, 254, 0.2); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                            ✨ AI-Powered
                        </span>
                        <span style="background: rgba(74, 172, 254, 0.2); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                            📚 NCERT Aligned
                        </span>
                        <span style="background: rgba(74, 172, 254, 0.2); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                            🇮🇳 Made in India
                        </span>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h3>📚 Learning</h3>
                    <a href="#learn">🧠 Interactive Learning</a>
                    <a href="#practice">📝 Practice Quizzes</a>
                    <a href="#curriculum">📖 NCERT Curriculum</a>
                    <a href="#progress">📊 Progress Tracking</a>
                    <a href="#achievements">🏆 Achievements</a>
                </div>
                
                <div class="footer-section">
                    <h3>🛠️ Resources</h3>
                    <a href="#help">❓ Help & Support</a>
                    <a href="#tutorials">🎥 Video Tutorials</a>
                    <a href="#api">🔧 API Documentation</a>
                    <a href="#changelog">📄 Changelog</a>
                    <a href="#feedback">💬 Feedback</a>
                </div>
                
                <div class="footer-section">
                    <h3>🤝 Community</h3>
                    <a href="#github">💻 Open Source</a>
                    <a href="#discord">💬 Discord Community</a>
                    <a href="#blog">📝 Blog</a>
                    <a href="#newsletter">📧 Newsletter</a>
                    <a href="#contribute">🤲 Contribute</a>
                </div>
            </div>
            
            <div class="footer-bottom">
                <div class="social-links">
                    <a href="#" class="social-link">📧</a>
                    <a href="#" class="social-link">🐱</a>
                    <a href="#" class="social-link">🐦</a>
                    <a href="#" class="social-link">💼</a>
                    <a href="#" class="social-link">📱</a>
                </div>
                
                <p style="margin: 1rem 0 0.5rem 0;">
                    <strong>© {current_year} ScienceGPT v3.0</strong> • 
                    Developed with ❤️ by <strong>Aseem Mehrotra</strong>
                </p>
                
                <p style="margin: 0; font-size: 0.9rem;">
                    🇮🇳 Proudly Indian • 
                    <a href="#privacy" style="color: #4facfe;">Privacy Policy</a> • 
                    <a href="#terms" style="color: #4facfe;">Terms of Service</a> • 
                    <a href="#contact" style="color: #4facfe;">Contact Us</a>
                </p>
                
                <p style="margin: 1rem 0 0 0; font-size: 0.8rem; opacity: 0.7;">
                    <em>"Making science education accessible for every Indian student"</em>
                </p>
            </div>
        </div>
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)


def render_mini_footer() -> None:
    """Render minimal footer for embedded usage"""
    
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1rem 0;
        color: #718096;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    ">
        <p style="margin: 0;">
            <strong>ScienceGPT v3.0</strong> • 
            Built with ❤️ by Aseem Mehrotra • 
            🇮🇳 Made in India
        </p>
    </div>
    """, unsafe_allow_html=True)
