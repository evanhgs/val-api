from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.core.config import fast_mqtt
from app.routes import auth, user, follow, post, like, comment, message
# from app.core.database import engine
# from app.models.models import Base

# la création des tables est gérée par Alembic (make migrate)
# Base.metadata.create_all(bind=engine)



@asynccontextmanager
async def _lifespan(_app: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()
app = FastAPI(
    title="Valenstagram API v2",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=_lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://app.evanh.site"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception processing request %s %s", request.method, request.url)
    headers = {"Access-Control-Allow-Origin": "https://app.evanh.site"}
    return JSONResponse(status_code=500, content={"status": "error", "detail": str(exc)}, headers=headers)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    print("Connected to MQTT Broker")
    client.subscribe("chat/+/messages")

@fast_mqtt.on_message()
async def messages(client, topic, payload, qos, properties):
    print(f"Message reçu: {payload} sur {topic}")

# Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(follow.router)
app.include_router(post.router)
app.include_router(like.router)
app.include_router(comment.router)
app.include_router(message.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur Valenstagram"}

@app.get("/health")
async def health_check():
    """Simple healthcheck utilisé par Docker Compose"""
    try:
        if not fast_mqtt.client.is_connected:
            return JSONResponse(status_code=500, content={"status": "degraded", "error": "MQTT not connected"})
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "degraded", "error": str(e)})

@app.get("/version")
def version():
    return {"version": "2.4.0"}
