# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="colombian-legal-scraper",
    version="1.0.0",
    author="Your Name",
    author_email="your-email@example.com",
    description="Automated system for scraping and analyzing Colombian legal documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/colombian-legal-db",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "legal-scraper=main:main",
        ],
    },
    include_package_data=True,
    keywords="colombia legal scraper laws ai nlp",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/colombian-legal-db/issues",
        "Source": "https://github.com/yourusername/colombian-legal-db",
    },
)
