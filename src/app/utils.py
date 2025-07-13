import time
import uuid

import streamlit as st
from extra_streamlit_components import CookieManager


def startup_page_ui() -> str:
    st.set_page_config(page_title='helpbot', page_icon='🤖')
    st.title('Customer support')

    cookie_manager = CookieManager()
    session_id: str = cookie_manager.get(cookie='ajs_anonymous_id')

    if session_id is None:
        session_id = str(uuid.uuid4())
        cookie_manager.set('ajs_anonymous_id', session_id)

    return session_id


def response_generator(response: str):
    for word in response.split():
        yield word + ' '
        time.sleep(0.05)
