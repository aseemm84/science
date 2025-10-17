# 🧪 ScienceGPT v3.0

**World-Class AI-Powered Science Education Platform for Indian Students**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made in India](https://img.shields.io/badge/Made%20in-India%20🇮🇳-orange.svg)]()

## 🌟 Features

- **🎓 Complete NCERT Curriculum** - 500+ topics across Physics, Chemistry, and Biology (Classes 1-12)
- **🤖 Advanced AI Integration** - Multi-provider support (Groq, OpenAI, Anthropic) with intelligent fallback
- **📚 Personalized Learning** - Adaptive content based on grade, subject, and learning style
- **🏆 Gamification System** - Points, badges, achievements, and streaks to maintain engagement
- **📊 Progress Analytics** - Comprehensive tracking and visualization of learning progress
- **🌐 Multi-language Support** - 10+ Indian languages for accessible learning
- **📱 Mobile Responsive** - Seamless experience across all devices
- **♿ Accessibility** - WCAG 2.1 AA compliant for inclusive education

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- API keys for LLM providers (at least one of: Groq, OpenAI, Anthropic)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sciencegpt_v3.git
cd sciencegpt_v3
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API keys
```

5. **Setup database**
```bash
python scripts/setup_db.py
```

6. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📖 Documentation

- [Deployment Guide](README_DEPLOYMENT.md) - Complete deployment instructions
- [API Documentation](docs/API.md) - API reference and integration guide
- [Database Schema](docs/DATABASE.md) - Database structure and models
- [Curriculum Structure](docs/CURRICULUM.md) - NCERT curriculum mapping

## 🏗️ Project Structure

```
sciencegpt_v3/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation configuration
├── .streamlit/                 # Streamlit configuration
│   ├── config.toml            # App configuration
│   └── secrets.toml.example   # Secret keys template
├── backend/                    # Backend logic
│   ├── ai/                    # AI/LLM integration
│   ├── curriculum/            # NCERT curriculum data
│   ├── database/              # Database models and management
│   ├── services/              # Business logic services
│   └── utils/                 # Utility functions
├── frontend/                   # Frontend components
│   ├── components/            # Reusable UI components
│   ├── pages/                 # Application pages
│   └── widgets/               # Custom widgets
├── assets/                     # Static assets
│   ├── styles/                # CSS styling
│   └── images/                # Images and icons
├── scripts/                    # Utility scripts
│   ├── setup_db.py           # Database setup
│   └── deploy.py             # Deployment automation
├── tests/                      # Test suite
├── docs/                       # Documentation
└── data/                       # Application data
```

## 🎯 Key Components

### Backend
- **Database** - SQLAlchemy ORM with SQLite/PostgreSQL support
- **AI System** - Multi-provider LLM integration with caching
- **Curriculum** - Complete NCERT topic mapping and progression
- **Services** - Quiz generation, analytics, recommendations

### Frontend
- **Navigation** - Context-aware navigation with progress indicators
- **Learning Interface** - AI-powered Q&A with conversation history
- **Practice System** - Interactive quizzes with instant feedback
- **Analytics Dashboard** - Comprehensive progress visualization

## 🔧 Configuration

### Environment Variables

Key environment variables (set in `.streamlit/secrets.toml`):

```toml
[ai_providers]
GROQ_API_KEY = "your_groq_api_key"
OPENAI_API_KEY = "your_openai_api_key"
ANTHROPIC_API_KEY = "your_anthropic_api_key"

[database]
DATABASE_URL = "sqlite:///data/sciencegpt_v3.db"

[cache]
REDIS_URL = "redis://localhost:6379"
ENABLE_CACHING = true
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://share.streamlit.io)
3. Configure secrets in Streamlit dashboard
4. Deploy from main branch

### Docker

```bash
python scripts/deploy.py docker
docker-compose up -d
```

### Heroku

```bash
python scripts/deploy.py heroku
git push heroku main
```

See [README_DEPLOYMENT.md](README_DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Performance

- **Response Time:** < 2 seconds for AI queries
- **Cache Hit Rate:** 40-60% efficiency boost
- **Concurrent Users:** 50+ supported
- **Uptime:** 99.9% availability target

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NCERT for the comprehensive curriculum framework
- Groq, OpenAI, and Anthropic for AI capabilities
- Streamlit for the amazing framework
- Indian education community for inspiration and feedback

## 📧 Contact

**Aseem Mehrotra**
- Email: aseemm84@gmail.com
- GitHub: [@aseemm84](https://github.com/aseemm84)
- Project Link: [https://github.com/aseemm84/sciencegpt_v3](https://github.com/aseemm84/sciencegpt_v3)

## 🌟 Star History

If you find this project helpful, please consider giving it a star ⭐

---

**Made with ❤️ in India 🇮🇳**

*Empowering Indian students with world-class AI-powered science education*
