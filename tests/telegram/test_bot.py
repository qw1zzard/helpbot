import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

os.environ['TELEGRAM_TOKEN'] = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'


class AsyncContextManagerMock:
    def __init__(self, return_value):
        self.return_value = return_value

    async def __aenter__(self):
        return self.return_value

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.mark.asyncio
@patch('src.telegram.bot.aiohttp.ClientSession')
async def test_handle_user_message_success(mock_client_session):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={'answer': 'Mocked answer'})

    mock_post_cm = AsyncContextManagerMock(mock_response)

    mock_session_instance = MagicMock()
    mock_session_instance.post.return_value = mock_post_cm

    mock_client_session.return_value.__aenter__.return_value = mock_session_instance

    mock_message = AsyncMock()
    mock_message.text = 'Hello'
    mock_message.answer = AsyncMock()

    from src.telegram.bot import handle_user_message

    await handle_user_message(mock_message)

    mock_message.answer.assert_called()
    assert 'Answer' in mock_message.answer.call_args[0][0]


@pytest.mark.asyncio
@patch('src.telegram.bot.aiohttp.ClientSession')
async def test_handle_user_message_api_error(mock_client_session):
    mock_response = AsyncMock()
    mock_response.status = 500

    mock_post_cm = AsyncContextManagerMock(mock_response)

    mock_session_instance = MagicMock()
    mock_session_instance.post.return_value = mock_post_cm

    mock_client_session.return_value.__aenter__.return_value = mock_session_instance

    mock_message = AsyncMock()
    mock_message.text = 'Hello'
    mock_message.answer = AsyncMock()

    from src.telegram.bot import handle_user_message

    await handle_user_message(mock_message)

    mock_message.answer.assert_called()
    assert 'Something went wrong' in mock_message.answer.call_args[0][0]


@pytest.mark.asyncio
@patch('src.telegram.bot.aiohttp.ClientSession')
async def test_handle_user_message_exception(mock_client_session):
    from src.telegram import bot

    mock_client_session.return_value.__aenter__.return_value.post.side_effect = (
        Exception('boom')
    )
    msg = AsyncMock()
    msg.text = 'hi'
    msg.answer = AsyncMock()
    await bot.handle_user_message(msg)
    msg.answer.assert_called()
    assert 'Error' in msg.answer.call_args[0][0]
