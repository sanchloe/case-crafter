import json
import os

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import Field
from langchain_databricks import ChatDatabricks
from openai import OpenAI
from pydantic import create_model

load_dotenv()

class CaseNotesGenerator:

    def __init__(self, transcript, template):
        self.transcript = transcript
        self.template = template
        self.endpoint_name= "databricks-meta-llama-3-1-70b-instruct"

    def create_dynamic_model(self):
        fields = {
            section: (str, Field(description=data['description'])) 
            for section, data in self.template['sections'].items()
        }

        CaseNotesModel = create_model(
            self.template['template_type'],  
            **fields
        )
        return CaseNotesModel

    def get_system_prompt(self):
        system_prompt = """You are an assistant for a mental health company. Your task is to review the audio transcription of a therapy session and generate case notes in first-person perspective, as if the therapist is personally writing them. Follow the specific template selected by the therapist for the session. Ensure the language used is professional, clear, and concise. Only include information explicitly mentioned in the audio, using direct quotes where appropriate to enhance accuracy. Avoid adding interpretations or assumptions beyond what was discussed in the session. Respond only with valid JSON. Do not write an introduction or summary.
        Here is a sample output for the SOAP template: 
        {{
            "Subjective": generated notes here,
            "Objective": generated notes here,
            "Assessment": generated notes here,
            "Plan": generated notes here
        }}
        """
        return system_prompt

    def create_user_prompt(self):
        user_prompt = "Here is the transcription of the therapy session: {transcript}"
        user_prompt += f"Now, fill out the following {self.template['template_type']} notes:\n"
        for section, data in self.template['sections'].items():
            user_prompt += f"{section.capitalize()} - {data['description']}: \n\n"
        user_prompt += "Respond only with valid JSON. Do not write an introduction or summary."
        user_prompt += """
        ```
        {format_instructions}
        ```"""
        return user_prompt

    def get_notes(self):
        model = ChatDatabricks(
            endpoint=self.endpoint_name,
            temperature=0.8,
            max_tokens=512,
        )

        case_notes_parser = JsonOutputParser(
            pydantic_object=self.create_dynamic_model())
        format_instructions = case_notes_parser.get_format_instructions()

        prompt = ChatPromptTemplate([("system", self.get_system_prompt()), 
                                     ("human", self.create_user_prompt())])
        chain = prompt | model | case_notes_parser
        input_dict = {
            "transcript": self.transcript, 
            "format_instructions": format_instructions
            }
        response = chain.invoke(input_dict)

        return response