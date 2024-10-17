from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import streamlit as st
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

CLIENT_CONFIG = st.secrets["google_oauth"]


def authenticate():
    if "auth_state" not in st.session_state:
        st.session_state.auth_state = "initial"

    if st.session_state.auth_state == "initial":
        flow = Flow.from_client_config(
            client_config=CLIENT_CONFIG,
            scopes=SCOPES,
            redirect_uri="https://gdrive-organizer.streamlit.app/callback"
        )
        authorization_url, _ = flow.authorization_url(prompt='consent')
        st.link_button("Click to Authorize", authorization_url)
        st.session_state.auth_state = "waiting_for_code"
        return None

    elif st.session_state.auth_state == "waiting_for_code":
        if "code" in st.experimental_get_query_params():
            flow = Flow.from_client_config(
                client_config=CLIENT_CONFIG,
                scopes=SCOPES,
                redirect_uri="https://gdrive-organizer.streamlit.app/callback"
            )
            flow.fetch_token(code=st.experimental_get_query_params()["code"][0])
            st.session_state.token = flow.credentials.to_json()
            st.session_state.auth_state = "authenticated"
            st.rerun()
        return None

    elif st.session_state.auth_state == "authenticated":
        return Credentials.from_authorized_user_info(json.loads(st.session_state.token))
