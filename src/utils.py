import json
import datetime
import uuid
import streamlit as st

from dotenv import load_dotenv
from langchain_databricks import ChatDatabricks

load_dotenv()

def read_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript = file.read()
    return transcript

def load_template(template_name):
    with open(f'{template_name}.json') as f:
        return json.load(f)
    
def load_model(endpoint, temperature):
    model = ChatDatabricks(
    endpoint = endpoint,
    temperature = temperature)
    return model

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name

def setup_session():
    client_name = "John Doe"
    client_id = str(uuid.uuid4())
    therapist_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    return session_id, therapist_id, client_id, client_name