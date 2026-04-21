"""
Setup script for NanoLandscape SaaS Platform
Advanced Nanoparticle Superspace Framework
"""

import os
from setuptools import setup, find_packages

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements from requirements.txt
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = f.read().splitlines()
    # Filter out empty lines and comments
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
    return requirements

setup(
    name="nanolandscape-saas",
    version="1.0.0",
    author="NanoLandscape Development Team",
    author_email="info@nanolandscape.ai",
    description="Advanced Nanoparticle Superspace Framework SaaS Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nanolandscape-saas-platform",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/nanolandscape-saas-platform/issues",
        "Documentation": "https://nanolandscape-saas-platform.readthedocs.io/",
        "Source Code": "https://github.com/yourusername/nanolandscape-saas-platform",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: FastAPI",
        "Environment :: Web Environment",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "pre-commit>=2.15.0",
            "tox>=3.24.0",
            "coverage>=5.5",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
        "gpu": [
            "cupy>=9.0.0",
            "nvidia-ml-py3>=7.352.0",
        ],
        "full": [
            "cupy>=9.0.0",
            "nvidia-ml-py3>=7.352.0",
            "ray>=1.6.0",
            "dask>=2021.9.0",
            "distributed>=2021.9.0",
        ],
        "web": [
            "jinja2>=3.0.0",
            "starlette>=0.14.0",
            "python-multipart>=0.0.5",
            "itsdangerous>=2.0.0",
        ],
        "visualization": [
            "plotly>=5.0.0",
            "bokeh>=2.4.0",
            "altair>=4.1.0",
            "folium>=0.12.0",
        ],
        "testing": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.0",
            "pytest-cov>=2.12.0",
            "httpx>=0.20.0",
            "responses>=0.14.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "sphinx-autodoc-typehints>=1.12.0",
            "myst-parser>=0.15.0",
            "sphinx-copybutton>=0.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nanolandscape=nanolandscape.cli.main:cli",
            "nanolandscape-server=nanolandscape.cli.main:serve",
            "nanolandscape-simulate=nanolandscape.cli.main:simulate",
        ],
    },
    keywords=[
        "nanoparticle",
        "superspace",
        "biological-modeling",
        "stochastic-differential-equations",
        "energy-landscape",
        "machine-learning",
        "scientific-computing",
        "biophysics",
        "drug-delivery",
        "nanomedicine",
        "pbpk",
        "protein-corona",
        "saas",
        "fastapi",
        "scientific-software",
    ],
    license="MIT License",
    license_files=("LICENSE",),
    zip_safe=False,
    platforms=["any"],
    dependency_links=[],
    setup_requires=[
        "setuptools>=45",
        "wheel>=0.37.0",
        "setuptools_scm[toml]>=6.2",
    ],
)