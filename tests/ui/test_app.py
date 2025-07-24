from unittest.mock import MagicMock, patch

import streamlit as st


@patch('src.ui.app.requests.post')
@patch('src.ui.app.response_generator', return_value=iter(['Answer']))
@patch('src.ui.app.st.chat_input', return_value='Question')
@patch('src.ui.app.startup_page_ui', return_value='test-session-id')
@patch('src.ui.app.st.write_stream')
@patch('src.ui.app.st.write')
@patch('src.ui.app.st.chat_message')
@patch('src.ui.app.st.spinner')
def test_streamlit_app_main(
    mock_spinner,
    mock_chat_msg,
    mock_write,
    mock_write_stream,
    mock_startup_ui,
    mock_chat_input,
    mock_resp_gen,
    mock_requests_post_success,
    clear_streamlit_state,
):
    mock_requests_post_success.return_value = MagicMock(
        status_code=200, json=lambda: {'answer': 'Answer'}
    )

    from src.ui.app import main

    main()

    messages = st.session_state.messages
    assert any(m['role'] == 'user' and m['content'] == 'Question' for m in messages)
    assert any(m['role'] == 'assistant' and 'Answer' in m['content'] for m in messages)
