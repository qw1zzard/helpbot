from unittest.mock import MagicMock, patch

import pytest
import streamlit as st


@pytest.fixture
def reset_streamlit_state():
    st.session_state.clear()


@patch('src.app.ui.requests.post')
@patch('src.app.ui.response_generator', return_value=iter(['Answer']))
@patch('src.app.ui.st.chat_input', return_value='Question')
@patch('src.app.ui.startup_page_ui', return_value='test-session-id')
@patch('src.app.ui.st.write_stream', return_value='Answer')
@patch('src.app.ui.st.write')
@patch('src.app.ui.st.chat_message')
@patch('src.app.ui.st.spinner')
def test_ui_main_success(
    mock_spinner,
    mock_chat_message,
    mock_write,
    mock_write_stream,
    mock_startup_page_ui,
    mock_chat_input,
    mock_response_generator,
    mock_requests_post,
    reset_streamlit_state,
):
    mock_requests_post.return_value = MagicMock(
        status_code=200, json=lambda: {'answer': 'Answer'}
    )

    from src.app.ui import main

    main()

    assert {'role': 'user', 'content': 'Question'} in st.session_state.messages

    mock_write_stream.assert_called()

    messages = [
        m['content'] for m in st.session_state.messages if m['role'] == 'assistant'
    ]
    assert any('Answer' in msg for msg in messages)
