from fastapi import FastAPI
from loguru import logger

from pokeai_api.routers.health import router as health_router


app = FastAPI()

app.include_router(health_router, prefix="/api")


# Startup event
@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    for router in app.routes:
        logger.info(f"Registered route: {router.methods} {router.path}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    # Do shutdown stuff here


@app.get("/")
async def root():
    return {"message": "Hello World"}
