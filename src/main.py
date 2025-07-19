from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.api.exceptions import validation_exception_handler
from src.api.router import router
from src.db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore


@app.get('/')
async def home():
    return 200


app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=80)
