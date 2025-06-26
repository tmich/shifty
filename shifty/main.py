import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from dotenv import load_dotenv
from shifty.api.routers import availabilities, shifts, overrides, users, auth, registration

# Load environment variables from .env file
load_dotenv()
from shifty.infrastructure.db import (
    admin_engine, 
    create_all_functions,
    create_all_security_policies,
    create_roles
)
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize database tables, functions, and security policies."""
    try:
        logger.info("Starting database initialization...")
        
        # Create all tables from SQLModel metadata
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(admin_engine)
        
        # Create database functions, security policies, and roles
        logger.info("Setting up database functions, policies, and roles...")
        with admin_engine.connect() as conn:
            create_all_functions(conn)
            create_all_security_policies(conn)
            create_roles(conn)
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def cleanup_database():
    """Cleanup database connections and resources."""
    try:
        logger.info("Cleaning up database resources...")
        # Close all connections in the engine pool
        admin_engine.dispose()
        logger.info("Database cleanup completed!")
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup and shutdown events."""
    # Startup
    try:
        # Only initialize database if not in test mode
        if not os.getenv("TESTING", "").lower() == "true":
            await initialize_database()
        logger.info("Application startup completed!")
        yield
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Application shutdown initiated...")
        if not os.getenv("TESTING", "").lower() == "true":
            await cleanup_database()
        logger.info("Application shutdown completed!")


# Create FastAPI app with lifespan management
app = FastAPI(
    title="Shifty API",
    description="A modern shift scheduling API with availability management and override handling",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
allowed_origins = [
    "http://localhost:3000",    # React dev server
    "http://localhost:5173",    # Vite dev server
    "http://localhost:8080",    # Alternative dev port
]

# Allow all origins in development, specific origins in production
if os.getenv("ENVIRONMENT", "development").lower() == "development":
    allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(availabilities.router, prefix="/api/v1", tags=["availabilities"])
app.include_router(shifts.router, prefix="/api/v1", tags=["shifts"])
app.include_router(overrides.router, prefix="/api/v1", tags=["overrides"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(registration.router, prefix="/api/v1", tags=["registration"])


@app.get("/", tags=["health"])
async def root():
    """Root endpoint for health checking."""
    return {
        "message": "Shifty API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check endpoint."""
    try:
        # Test database connection
        with admin_engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"  # You might want to use datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }


# For backwards compatibility when running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    
    # Initialize database for direct execution
    import asyncio
    asyncio.run(initialize_database())
    
    # Run the server
    uvicorn.run(
        "shifty.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )