import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from app.api.platform.router import router as platform_router
from app.config import settings
from app.exceptions import APIException


def route_operation_id(route: APIRoute) -> str:
    # Use the endpoint function name as the operationId instead of FastAPI's
    # default "{name}_{path}_{method}". This keeps the generated frontend client
    # readable (e.g. useGetCurrentUser instead of useGetCurrentUserUsersMeGet).
    # Endpoint function names within each sub-app are unique, so no collisions.
    return route.name


app = FastAPI(
    title=settings.PROJECT_NAME,
)

platform_api = FastAPI(
    contact={"name": "Chamoda Pandithage", "email": "chamoda@xaventra.com"},
    description="Platform api endpoints",
    generate_unique_id_function=route_operation_id,
    openapi_tags=[
        {"name": "meta", "description": "Health and service metadata"},
        {"name": "auth", "description": "Authentication and session"},
        {"name": "users", "description": "User endpoints"},
    ],
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
