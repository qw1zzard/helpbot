import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from src.api.exceptions import validation_exception_handler
from starlette.datastructures import Headers


@pytest.mark.asyncio
async def test_validation_exception_handler_returns_json():
    errors = [
        {
            'type': 'string_type',
            'loc': ['body', 'name'],
            'msg': 'Input should be a valid string',
            'input': 123,
        }
    ]
    request = Request(scope={'type': 'http', 'headers': Headers().raw})
    exc = RequestValidationError(errors=errors)

    response = await validation_exception_handler(request, exc)

    assert response.status_code == 422
    assert response.headers['content-type'] == 'application/json'
    body = response.body.decode()  # type: ignore
    assert 'Unprocessable Entity' in body
    assert 'errors' in body
