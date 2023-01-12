from beanie import init_beanie
from fastapi import FastAPI
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from pokeai_api.config import settings
from pokeai_api.models import PokemonODM
from pokeai_api.routers.health import router as health_router
from pokeai_api.routers.pokemon import router as pokemon_router


app = FastAPI()


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

    app.include_router(health_router, prefix="/api")
    app.include_router(pokemon_router, prefix="/api")

    client = AsyncIOMotorClient(
        f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}"
        f"@{settings.MONGO_HOST}:{settings.MONGO_PORT}"
    )

    await init_beanie(
        database=client.pokeai,
        document_models=[PokemonODM],
    )

    for router in app.routes:
        logger.info(f"Registered route: {router.methods} {router.path}")

    logger.info("Startup complete.")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    # Do shutdown stuff here
    logger.info("Shutdown complete.")


@app.get("/")
async def root():
    return {"message": "Hello World"}
