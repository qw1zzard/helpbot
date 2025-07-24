import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from src.api.exceptions import validation_exception_handler
from starlette.datastructures import Headers


@pytest.mark.asyncio
async def test_validation_exception_handler():
    errors = [
        {
            'type': 'string_type',
            'loc': ['body', 'name'],
            'msg': 'Input should be a valid string',
            'input': 123,
        }
    ]
    exc = RequestValidationError(errors=errors)

    request = Request(scope={'type': 'http', 'headers': Headers().raw})

    response = await validation_exception_handler(request, exc)
    data = response.body.decode()  # type: ignore

    assert response.status_code == 422
    assert response.headers['content-type'] == 'application/json'
    assert 'Unprocessable Entity' in data
    assert 'errors' in data
