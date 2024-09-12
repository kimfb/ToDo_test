import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings
from db import BaseDBModel, db_helper
from api import router as router_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)
        yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
