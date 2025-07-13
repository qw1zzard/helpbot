import requests
import streamlit as st
from app.utils import response_generator, startup_page_ui


def main():
    session_id = startup_page_ui()

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {'role': 'assistant', 'content': 'How can I help you?'}
        ]

    if prompt := st.chat_input('Enter your question'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if st.session_state.messages[-1]['role'] != 'assistant':
        with st.chat_message('assistant'):
            with st.spinner('Gathering information'):
                history_message = {
                    'session_id': session_id,
                    'history': [{'role': 'user', 'content': prompt}],
                }

                try:
                    response = requests.post(
                        'http://localhost:80/api/v1/get_answer/',
                        json=history_message,
                    )
                    response.raise_for_status()
                    answer = response.json()

                    response = st.write_stream(response_generator(answer['answer']))
                    st.session_state.messages.append(
                        {'role': 'assistant', 'content': response}  # type: ignore
                    )

                except requests.exceptions.RequestException as e:
                    st.error(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
