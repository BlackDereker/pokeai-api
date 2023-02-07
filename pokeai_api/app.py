from beanie import init_beanie
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.routing import Mount

from pokeai_api.config import settings
from pokeai_api.models import PokemonODM
from pokeai_api.routers.health import router as health_router
from pokeai_api.routers.pokemon import router as pokemon_router


app = FastAPI(debug=settings.LOG_LEVEL == "DEBUG")

# app.add_middleware(
#     PyInstrumentProfilerMiddleware,
#     server_app=app,  # Required to output the profile on server shutdown
#     profiler_output_type="html",
#     is_print_each_request=False,  # Set to True to show request profile on
#                                   # stdout on each request
#     open_in_browser=False,  # Set to true to open your web-browser automatically
#                             # when the server shuts down
# )

app.add_middleware(DebugToolbarMiddleware)


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
        if isinstance(router, Mount):
            logger.info(f"Registered mount: {router.name}")
        else:
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
