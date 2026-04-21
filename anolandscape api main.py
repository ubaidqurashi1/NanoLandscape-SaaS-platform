# nanolandscape/api/main.py
"""
FastAPI main application for NanoLandscape SaaS
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
import asyncio
import uuid
from datetime import datetime
import logging
import numpy as np

from ..core.engine import SuperspaceEngine
from ..services.designer import NPDesignerPro
from ..services.analyzer import HeterogeneityAnalyzer
from ..services.optimizer import ControlOptimizer
from ..services.predictor import FatePredictor
from ..data.database import NPDatabase

app = FastAPI(
    title="NanoLandscape SaaS API",
    description="Advanced Nanoparticle Superspace Framework API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
engine = SuperspaceEngine()
designer = NPDesignerPro(engine)
analyzer = HeterogeneityAnalyzer(engine)
optimizer = ControlOptimizer(engine)
predictor = FatePredictor(engine)
database = NPDatabase()

# Pydantic models
class NPParameters(BaseModel):
    core: Dict = Field(..., description="Core nanoparticle parameters")
    surface: Dict = Field(..., description="Surface parameters")
    corona: Dict = Field(..., description="Corona composition parameters")
    context: Dict = Field(..., description="Environmental context parameters")
    spatial: Dict = Field(..., description="Spatial positioning parameters")

class SimulationRequest(BaseModel):
    np_parameters: NPParameters
    time_horizon: float = Field(default=3600.0, description="Simulation time in seconds")
    ensemble_size: int = Field(default=100, description="Number of particles in ensemble")
    noise_level: float = Field(default=0.01, description="Initial condition noise level")
    lambda_params: Dict = Field(default={}, description="Control parameters")

class DesignRequest(BaseModel):
    target_organ: str
    desired_fate: str
    constraints: Dict
    batch_variability_limit: float = 0.05

class AnalysisRequest(BaseModel):
    simulation_results: Dict
    analysis_type: str = "heterogeneity"

@app.get("/")
async def root():
    return {"message": "Welcome to NanoLandscape SaaS API", "version": "1.0.0"}

@app.post("/simulate")
async def simulate_nanoparticles(request: SimulationRequest):
    """Run nanoparticle simulation using the superspace framework"""
    try:
        # Construct state vector
        state_vector = engine.construct_state_vector(
            request.np_parameters.core,
            request.np_parameters.surface,
            request.np_parameters.corona,
            request.np_parameters.context,
            request.np_parameters.spatial
        )
        
        # Generate initial conditions
        initial_conditions = engine.generate_initial_conditions(
            state_vector, request.ensemble_size, request.noise_level
        )
        
        # Time points
        time_points = np.linspace(0, request.time_horizon, 
                                int(request.time_horizon / engine.config['dt']) + 1)
        
        # Solve SDE
        trajectories = engine.solve_stochastic_differential_equation(
            initial_conditions, time_points, request.lambda_params
        )
        
        # Reconstruct energy landscape
        landscape_data = engine.reconstruct_energy_landscape(trajectories)
        
        # Prepare response
        result = {
            "simulation_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "trajectories": trajectories.tolist(),
            "time_points": time_points.tolist(),
            "landscape": landscape_data,
            "summary_statistics": {
                "mean_final_positions": np.mean(trajectories[:, -1, :], axis=0).tolist(),
                "std_final_positions": np.std(trajectories[:, -1, :], axis=0).tolist(),
                "ensemble_size": request.ensemble_size,
                "time_horizon": request.time_horizon
            }
        }
        
        # Store in database
        await database.store_simulation(result)
        
        return result
        
    except Exception as e:
        logging.error(f"Simulation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.post("/design/nanoparticle")
async def design_nanoparticle(request: DesignRequest):
    """Design optimal nanoparticle for specific target"""
    try:
        result = designer.optimize_design(
            target_organ=request.target_organ,
            desired_fate=request.desired_fate,
            constraints=request.constraints,
            batch_variability_limit=request.batch_variability_limit
        )
        
        return result
        
    except Exception as e:
        logging.error(f"Design error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Design failed: {str(e)}")

@app.post("/analyze/heterogeneity")
async def analyze_heterogeneity(request: AnalysisRequest):
    """Analyze batch heterogeneity and variance amplification"""
    try:
        if request.analysis_type == "heterogeneity":
            result = analyzer.analyze_batch_heterogeneity(request.simulation_results)
        else:
            raise ValueError(f"Unknown analysis type: {request.analysis_type}")
        
        return result
        
    except Exception as e:
        logging.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/optimize/control")
async def optimize_control_parameters(request: SimulationRequest):
    """Optimize control parameters for desired outcome"""
    try:
        result = optimizer.optimize_control(
            request.np_parameters,
            request.lambda_params
        )
        
        return result
        
    except Exception as e:
        logging.error(f"Optimization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.post("/predict/fate")
async def predict_biodistribution(request: SimulationRequest):
    """Predict nanoparticle biodistribution and fate"""
    try:
        result = predictor.predict_fate(
            request.np_parameters,
            request.time_horizon
        )
        
        return result
        
    except Exception as e:
        logging.error(f"Fate prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fate prediction failed: {str(e)}")