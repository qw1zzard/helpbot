from contextlib import asynccontextmanager

import uvicorn
from api.router import router
from db.database import create_tables, delete_tables
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await delete_tables()


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def home():
    return 200


app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=80)
