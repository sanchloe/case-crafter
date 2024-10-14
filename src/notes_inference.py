from typing import List

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from src.utils import load_model

class Notes(BaseModel):

    client_presentation: List = Field(description="Client's presentation")
    response_to_treatment: List = Field(description="Client's response to treatment")
    client_status: List = Field(description="Client's Status")
    risk_assessment: List = Field(description="Risk Assessment of client done by therapist")

class ProgressNotesJSON(BaseModel):

    progress_notes: List[Notes]

output_parser = JsonOutputParser(pydantic_object=ProgressNotesJSON)
format_instructions = output_parser.get_format_instructions()

class ProgressNotes:
    def __init__(self, transcript):
        self.model = load_model(endpoint = "databricks-meta-llama-3-1-70b-instruct", temperature=0.5)
        self.transcript = transcript

    def run_progress_notes(self):
        template = f"""You will be provided with a transcript. Your task is to classify the transcript based on four main categories: Client Presentation, Response to Treatment, Client Status, and Risk Assessment.
        You are a mental health assistant designed to analyze and categorize a client's sentiment, mood, and progress based on a transcript of conversations between the therapist and the patient. You must answer in a valid JSON format.

        Here are the steps to follow:

        Client Presentation: Identify the client's emotional state(s) by selecting the most appropriate item(s) from the list below.

        Options: 'Anxious', 'Confused', 'Energetic', 'Worried', 'Fearful', 'Cooperative', 'Withdrawn', 'Lethargic', 'Relaxed', 'Depressed'
        Response to Treatment: Determine the client's response to their treatment by choosing the most fitting option(s).

        Options: 'Cooperative', 'Uninterested', 'Receptive', 'Combative', 'Engaged'
        Client Status: Assess the current status of the client and select the item(s) that best describe it.

        Options: 'Improving', 'Unchanged', 'Regressed', 'Deteriorating'
        Risk Assessment: Evaluate any potential risks and choose the most suitable description(s) from the options given.

        Options: 'Attempted to Cause Harm', 'Intention to cause harm', 'Suicidal ideation', 'Danger to self', 'Danger to others', 'Plan to cause harm'
        For each main category, select one or more item only from the provided options that best reflects the contents of the transcript. If no item is selected for a category, return an empty string for that field.

        ***Format Instruction: Structure your output into a json format for each field.  Make Sure the JSON is valid.***
        ```
        {{format_instructions}}
        ```
        Please analyze the following transcript carefully:
        {{transcript}}

        Based on the analysis, please list the selected items under each category."""  
        system_prompt = "You are a mental health assistant designed to analyze and categorize a client's sentiment, mood, and progress based on a transcript of conversations between the therapist and the patient. You must answer in a valid JSON format."
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", template)])
        chain = prompt | self.model | output_parser
        input_dict = {"transcript": self.transcript, "format_instructions": format_instructions}
        response = chain.invoke(input_dict)
        return response