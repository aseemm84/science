"""
Setup script for ScienceGPT v3.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="sciencegpt-v3",
    version="3.0.0",
    author="Aseem Mehrotra",
    author_email="your.email@example.com",
    description="World-Class AI-Powered Science Education Platform for Indian Students",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aseemm84/sciencegpt_v3",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.3.3",
            "pytest-asyncio>=0.24.0",
            "pytest-cov>=6.0.0",
            "black>=24.10.0",
            "flake8>=7.1.1",
            "mypy>=1.13.0",
        ],
        "production": [
            "gunicorn>=23.0.0",
            "uvicorn>=0.32.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sciencegpt=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/**/*", ".streamlit/*", "docs/*"],
    },
)
