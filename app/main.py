from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.core.config import settings
from repos.api.v1 import router as repos_router
from repos.models import Base as OrgBase

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app

OrgBase.metadata.create_all(bind=engine)

app = get_application()
app.include_router(repos_router, prefix="/api")