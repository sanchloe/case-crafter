import json

def read_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript = file.read()
    return transcript

def load_template(template_name):
    with open(f'{template_name}.json') as f:
        return json.load(f)