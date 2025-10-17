"""
Deployment Script for ScienceGPT v3.0
Automated deployment to various platforms
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List


class DeploymentManager:
    """Manages deployment to different platforms"""
    
    def __init__(self):
        """Initialize deployment manager"""
        self.project_root = Path(__file__).parent.parent
        self.app_name = "sciencegpt-v3"
        
    def deploy_to_streamlit_cloud(self) -> bool:
        """Deploy to Streamlit Cloud"""
        
        print("☁️ Deploying to Streamlit Cloud...")
        
        # Check requirements
        if not self._check_streamlit_requirements():
            return False
        
        # Validate configuration
        if not self._validate_config():
            return False
        
        print("✅ Ready for Streamlit Cloud deployment")
        print("📋 Manual steps required:")
        print("  1. Push code to GitHub repository")
        print("  2. Connect repository to Streamlit Cloud")
        print("  3. Configure secrets in Streamlit Cloud dashboard")
        print("  4. Deploy from main branch")
        
        return True
    
    def deploy_to_heroku(self) -> bool:
        """Deploy to Heroku"""
        
        print("🚀 Preparing Heroku deployment...")
        
        # Create Procfile
        self._create_procfile()
        
        # Create runtime.txt
        self._create_runtime_file()
        
        # Create Heroku configuration
        heroku_config = self._get_heroku_config()
        
        print("✅ Heroku deployment files created")
        print("📋 Run these commands to deploy:")
        print("  heroku create your-app-name")
        print("  git add . && git commit -m 'Deploy to Heroku'")
        print("  git push heroku main")
        
        for key, value in heroku_config.items():
            print(f"  heroku config:set {key}='{value}'")
        
        return True
    
    def deploy_to_docker(self) -> bool:
        """Create Docker deployment"""
        
        print("🐳 Creating Docker deployment...")
        
        # Create Dockerfile
        self._create_dockerfile()
        
        # Create docker-compose.yml
        self._create_docker_compose()
        
        # Create .dockerignore
        self._create_dockerignore()
        
        print("✅ Docker deployment files created")
        print("📋 Run these commands to deploy:")
        print("  docker-compose build")
        print("  docker-compose up -d")
        
        return True
    
    def _check_streamlit_requirements(self) -> bool:
        """Check Streamlit Cloud requirements"""
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        # Check for main app file
        if not (self.project_root / "app.py").exists():
            print("❌ app.py not found")
            return False
        
        return True
    
    def _validate_config(self) -> bool:
        """Validate configuration files"""
        
        config_file = self.project_root / ".streamlit" / "config.toml"
        secrets_example = self.project_root / ".streamlit" / "secrets.toml.example"
        
        if not config_file.exists():
            print("⚠️ .streamlit/config.toml not found")
        
        if not secrets_example.exists():
            print("⚠️ .streamlit/secrets.toml.example not found")
        
        return True
    
    def _create_procfile(self):
        """Create Procfile for Heroku"""
        
        procfile_content = """web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
"""
        
        procfile_path = self.project_root / "Procfile"
        with open(procfile_path, 'w') as f:
            f.write(procfile_content)
        
        print("  ✅ Created Procfile")
    
    def _create_runtime_file(self):
        """Create runtime.txt for Heroku"""
        
        runtime_content = "python-3.11.7\n"
        
        runtime_path = self.project_root / "runtime.txt"
        with open(runtime_path, 'w') as f:
            f.write(runtime_content)
        
        print("  ✅ Created runtime.txt")
    
    def _get_heroku_config(self) -> Dict[str, str]:
        """Get Heroku configuration variables"""
        
        return {
            "GROQ_API_KEY": "your_groq_api_key",
            "OPENAI_API_KEY": "your_openai_api_key",
            "DATABASE_URL": "sqlite:///data/sciencegpt.db",
            "PYTHONPATH": "/app"
        }
    
    def _create_dockerfile(self):
        """Create Dockerfile"""
        
        dockerfile_content = """# ScienceGPT v3.0 - Docker Configuration
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data backups

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
        
        dockerfile_path = self.project_root / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        print("  ✅ Created Dockerfile")
    
    def _create_docker_compose(self):
        """Create docker-compose.yml"""
        
        compose_content = """version: '3.8'

services:
  sciencegpt:
    build: .
    ports:
      - "8501:8501"
    environment:
      - PYTHONPATH=/app
      - DATABASE_URL=sqlite:///data/sciencegpt_v3.db
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./backups:/app/backups
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
"""
        
        compose_path = self.project_root / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        
        print("  ✅ Created docker-compose.yml")
    
    def _create_dockerignore(self):
        """Create .dockerignore"""
        
        dockerignore_content = """.git
.gitignore
README.md
Dockerfile
.dockerignore
.streamlit/secrets.toml
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.DS_Store
.vscode/
.idea/
"""
        
        dockerignore_path = self.project_root / ".dockerignore"
        with open(dockerignore_path, 'w') as f:
            f.write(dockerignore_content)
        
        print("  ✅ Created .dockerignore")


def main():
    """Main deployment function"""
    
    print("🚀 ScienceGPT v3.0 - Deployment Manager")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <platform>")
        print("Platforms: streamlit, heroku, docker, all")
        sys.exit(1)
    
    platform = sys.argv[1].lower()
    deployment_manager = DeploymentManager()
    
    success = True
    
    if platform == "streamlit" or platform == "all":
        success &= deployment_manager.deploy_to_streamlit_cloud()
    
    if platform == "heroku" or platform == "all":
        success &= deployment_manager.deploy_to_heroku()
    
    if platform == "docker" or platform == "all":
        success &= deployment_manager.deploy_to_docker()
    
    if success:
        print("🎉 Deployment preparation completed successfully!")
    else:
        print("❌ Deployment preparation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
