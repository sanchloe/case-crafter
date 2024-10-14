import json
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
