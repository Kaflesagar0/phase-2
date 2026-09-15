from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from src.infrastructure.settings import settings
from src.interfaces.api.health import router as health_router
from src.interfaces.api.sensors import router as sensors_router



app = FastAPI(
    title="Smart Greenhouse API",
    version="0.1.0",
    docs_url=None,    # Explicitly disables /docs (Swagger)
    redoc_url=None,   # Explicitly disables /redoc
)

app.include_router(sensors_router)

# Configure CORS
origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root discovery endpoint
@app.get("/", include_in_schema=False)
def root_discovery():
    return {
        "service": "Smart Greenhouse API",
        "docs": "/scalar",
        "openapi": "/openapi.json",
        "health": "/health",
    }

# Mount Scalar API reference
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

# Include API routes
app.include_router(health_router)
