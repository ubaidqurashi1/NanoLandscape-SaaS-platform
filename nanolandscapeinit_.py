# nanolandscape/__init__.py
"""
NanoLandscape SaaS Platform - Full Implementation
Advanced Nanoparticle Superspace Framework
"""

__version__ = "1.0.0"
__author__ = "NanoLandscape Development Team"

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .core.engine import SuperspaceEngine
from .api.main import app
from .services.designer import NPDesignerPro
from .services.analyzer import HeterogeneityAnalyzer
from .services.optimizer import ControlOptimizer
from .services.predictor import FatePredictor
from .data.database import NPDatabase
from .models.landscape import LandscapeConstructor
from .simulation.solver import StochasticSolver
from .utils.validation import validate_model

def create_app():
    """Create and configure the FastAPI application."""
    return app