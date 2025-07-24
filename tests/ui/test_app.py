from unittest.mock import MagicMock, patch

import pytest
import streamlit as st


@pytest.fixture
def reset_streamlit_state():
    st.session_state.clear()


@patch('src.ui.app.requests.post')
@patch('src.ui.app.response_generator', return_value=iter(['Answer']))
@patch('src.ui.app.st.chat_input', return_value='Question')
@patch('src.ui.app.startup_page_ui', return_value='test-session-id')
@patch('src.ui.app.st.write_stream', return_value='Answer')
@patch('src.ui.app.st.write')
@patch('src.ui.app.st.chat_message')
@patch('src.ui.app.st.spinner')
def test_streamlit_ui_main(
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

    from src.ui.app import main

    main()

    assert {'role': 'user', 'content': 'Question'} in st.session_state.messages
    assert any(
        m['role'] == 'assistant' and 'Answer' in m['content']
        for m in st.session_state.messages
    )
