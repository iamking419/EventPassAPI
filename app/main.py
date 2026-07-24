from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, students, verify, logs,stats

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventPass API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow every frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE...
    allow_headers=["*"],  # Authorization, Content-Type...
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(verify.router, prefix="/api/v1/verify", tags=["Verify"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["Logs"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Stats"])


# -----------------------------
# Swagger / OpenAPI FIX
# -----------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="0.1.0",
        description="EventPass API",
        routes=app.routes,
    )

    # Ensure securitySchemes exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    # Force clean Bearer-only auth (NO OAuth flow confusion)
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# -----------------------------
# Root route
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "EventPass API Running"
    }
