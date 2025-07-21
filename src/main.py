from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.api.exceptions import validation_exception_handler
from src.api.router import router
from src.core.model import populate_if_empty, recreate_collection_if_needed
from src.db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    recreate_collection_if_needed()
    populate_if_empty()
    yield


app = FastAPI(
    title='helpbot',
    description='Q&A assistant',
    version='1.0.0',
    lifespan=lifespan,
)
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore


@app.get('/')
async def home():
    return {'status': 'ok'}


app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=80)
