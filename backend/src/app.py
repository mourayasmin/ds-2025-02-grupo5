"""FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import (
    escola_router,
    estudante_router,
    inscricao_router,
    equipe_router,
    equipe_membro_router,
)

app = FastAPI(
    title="Highschool AI Olympics Subscription API",
    description="API for managing subscriptions to the Highschool AI Olympics in Goiás, Brazil",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(escola_router)
app.include_router(estudante_router)
app.include_router(inscricao_router)
app.include_router(equipe_router)
app.include_router(equipe_membro_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Highschool AI Olympics Subscription API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

