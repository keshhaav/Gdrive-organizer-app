from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import streamlit as st
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

CLIENT_CONFIG = st.secrets["google_oauth"]


def authenticate():
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri="https://gdrive-organizer.streamlit.app/callback"
    )

    if "token" not in st.session_state:
        if "code" not in st.experimental_get_query_params():
            authorization_url, _ = flow.authorization_url(prompt='consent')
            st.link_button("Click to Authorize", authorization_url)
            
            return None
        else:
            flow.fetch_token(code=st.experimental_get_query_params()["code"][0])
            st.session_state.token = flow.credentials.to_json()
            st.rerun()

    return Credentials.from_authorized_user_info(json.loads(st.session_state.token))