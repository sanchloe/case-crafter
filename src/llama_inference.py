import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DATABRICKS_TOKEN"),
    base_url="https://dbc-1d50e92c-2c27.cloud.databricks.com/serving-endpoints"
)

class CaseNotesGenerator:

    def __init__(self, transcription, template):
        self.transcription = transcription
        self.template = template

    def get_system_prompt(self):
        system_prompt = """You are an assistant for a mental health company. Your task is to review the audio transcription of a therapy session and generate case notes in first-person perspective, as if the therapist is personally writing them. Follow the specific template selected by the therapist for the session. Ensure the language used is professional, clear, and concise. Only include information explicitly mentioned in the audio, using direct quotes where appropriate to enhance accuracy. Avoid adding interpretations or assumptions beyond what was discussed in the session. Respond only with valid JSON. Do not write an introduction or summary.
        Here is a sample output for the SOAP template: 
        {
            "Subjective": generated notes here,
            "Objective": generated notes here,
            "Assessment": generated notes here,
            "Plan": generated notes here
        }
        """
        return system_prompt

    def create_user_prompt(self):

        user_prompt = f"Here is the transcription of the therapy session:\n{self.transcription}\n\n"
        user_prompt += f"Now, fill out the following {self.template['template_type']} notes:\n"
        for section, data in self.template['sections'].items():
            user_prompt += f"{section.capitalize()} - {data['description']}: \n\n"
        user_prompt += "Respond only with valid JSON. Do not write an introduction or summary."

        return user_prompt
    
    def convert_to_json(self, notes):

        try:
            return json.loads(notes)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except:
            raise

    def get_notes(self):
        chat_completion = client.chat.completions.create(
            messages=[
            {
                "role": "system",
                "content": self.get_system_prompt()
            },
            {
                "role": "user",
                "content": self.create_user_prompt()
            }
            ],
                model="databricks-meta-llama-3-1-70b-instruct",
                max_tokens=512
            )

        notes = self.convert_to_json(chat_completion.choices[0].message.content)
        return notes