import json
from dotenv import load_dotenv
from langchain_databricks import ChatDatabricks
import datetime
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

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name