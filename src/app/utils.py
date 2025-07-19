import time
import uuid

import streamlit as st


def startup_page_ui() -> str:
    st.set_page_config(page_title='helpbot', page_icon='🤖')
    st.title('Customer support')

    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    return st.session_state.session_id


def response_generator(response: str):
    for word in response.split():
        yield word + ' '
        time.sleep(0.05)
