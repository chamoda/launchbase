import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.platform.router import router as platform_router
from app.config import settings
from app.exceptions import APIException

app = FastAPI(
    title=settings.PROJECT_NAME,
)

platform_api = FastAPI(
    contact={"name": "Chamoda Pandithage", "email": "chamoda@xaventra.com"},
    description="Platform api endpoints",
    openapi_tags=[{"name": "platform", "description": "Platform enpoints"}],
)


@platform_api.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return exc.to_response()


platform_api.include_router(platform_router)
platform_api.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/platform", platform_api, "platform")


obj_dir = os.path.join(os.getcwd(), "obj")
if os.path.exists(obj_dir):
    app.mount("/obj", StaticFiles(directory="obj"), name="obj")
