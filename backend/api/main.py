"""
Aplicación principal FastAPI para el sistema de agentes LLM personalizables
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from .endpoints import agent_endpoints

# Crear aplicación FastAPI
app = FastAPI(
    title="Habilitación LLM - Agentes Legales",
    description="Sistema de agentes legales personalizables con LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://legal-search-frontend-prod-wrvcg.ondigitalocean.app",
        "https://legal-search-frontend-staging-ooma3.ondigitalocean.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(agent_endpoints.router)


@app.get("/")
async def root():
    """
    Endpoint raíz
    """
    return {
        "message": "Habilitación LLM - Sistema de Agentes Legales",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "habilitacion-llm",
        "version": "1.0.0"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Manejador de excepciones HTTP
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Manejador de excepciones generales
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
