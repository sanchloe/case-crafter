import json
import streamlit as st

from src import llama_inference
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Case Crafter",layout="wide")

template_dict = {
    "SOAP": "soap.json",
    "DAP": "dap.json",
    "BIRP": "birp.json"
}

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('./src/css_styles/style.css')

try:
    st.markdown("<h1 style='text-align: center;'>Case Crafter</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Your AI Therapist Ally</h2>", unsafe_allow_html=True)
    st.markdown("---")

    audio_col, template_col= st.columns(spec=2,gap="large")
    with audio_col:
        audio_file = None
        st.subheader("Upload Audio")
        audio_file = st.file_uploader("Upload an audio file", type=["mp3"])

    with template_col:
        st.subheader("Template Style")
        user_template_option = st.selectbox('Select your preferred template style',('SOAP', 'DAP', 'BIRP'))
        st.write('You selected:', user_template_option)
        submit_button = st.button("Submit", key="submit_button")
    st.markdown("---")

    progress_col, output_col= st.columns(spec=2,gap="large")
    with progress_col:
        st.subheader("Progress Notes")
        st.markdown("#### Client Presentation")
        option_1 = st.checkbox('Anxious')
        option_2 = st.checkbox('Confused')
        option_3 = st.checkbox('Energetic')
        option_4 = st.checkbox('Worried')
        option_5 = st.checkbox('Fearful')
        option_6 = st.checkbox('Cooperative', key="cooperative_1")
        option_7 = st.checkbox('Withdrawn')
        option_8 = st.checkbox('Lethargic')
        option_9 = st.checkbox('Relaxed')
        option_10 = st.checkbox('Depressed')
        st.text("Recommended: ")

        st.markdown('#### Response to Treatment')
        option_11 = st.checkbox('Cooperative', key="cooperative_2")
        option_12 = st.checkbox('Uninterested')
        option_13 = st.checkbox('Receptive')
        option_14 = st.checkbox('Combative')
        option_15 = st.checkbox('Engaged')
        st.markdown('<p>Recommended: <span class="recommendedtext">Engaged</span> <span class="recommendedtext">Receptive</span></p>', unsafe_allow_html=True) #supposed to be dynamic based on llm output

        st.markdown('#### Interventions Used')
        checks = st.columns(3)
        with checks[0]:
            option_22 = st.checkbox('Cognitive Restructuring')
            option_23 = st.checkbox('DBT')
            option_24 = st.checkbox('Communication Training')
            option_25 = st.checkbox('EMDR')
            option_26 = st.checkbox('Assessment')
            option_27 = st.checkbox('CBT')
            option_28 = st.checkbox('Client Centered Therapy')
            option_29 = st.checkbox('Exploration')
            option_30 = st.checkbox('Anger Management')
            option_31 = st.checkbox('Behavior Reinforcement')
            option_32 = st.checkbox('Crisis Intervention')
            option_33 = st.checkbox('Developed Coping Skills')
            st.text("Recommended: ")
        with checks[1]:
            option_34 = st.checkbox('Emotion-Focused Therapy')
            option_35 = st.checkbox('Build rapport')
            option_36 = st.checkbox('Boundary Setting')
            option_37 = st.checkbox('Clinical Challenging')
            option_38 = st.checkbox('ACT')
            option_39 = st.checkbox('Somatic Therapy')
            option_40 = st.checkbox('Role Play')
            option_41 = st.checkbox('Psychoeducation')
            option_42 = st.checkbox('Exposure Therapy')
            option_43 = st.checkbox('Problem-Solving Therapy')
            option_44 = st.checkbox('Goal/Progress Review')
        with checks[2]:
            option_45 = st.checkbox('Interpersonal Therapy')
            option_46 = st.checkbox('Mindfulness')
            option_47 = st.checkbox('Stress Management')
            option_48 = st.checkbox('Grief Counseling')
            option_49 = st.checkbox('Motivational Interviewing')
            option_50 = st.checkbox('Trauma Therapy')
            option_51 = st.checkbox('Positive Psychology')
            option_52 = st.checkbox('Social Skills Training')
            option_53 = st.checkbox('Safety Planning')
            option_54 = st.checkbox('Psychodynamic Therapy')
            option_55 = st.checkbox('Reflective Listening')

    with output_col:
        section_lst = []
        description_lst = []
        st.subheader("Case Notes")
        if user_template_option in template_dict:
            json_template_file = template_dict[user_template_option]
        json_file = "./src/dependencies/{}".format(json_template_file)
        with open(json_file, 'r') as file:
            data = json.load(file)
            for section, details in data['sections'].items():
                section_lst.append(section)
                description_lst.append(details['description'])

        placeholders = {}
        if len(section_lst) > 0 and len(description_lst) > 0: 
            for key, description in zip(section_lst, description_lst):
                print(f"{key}")
                print(f"{description}\n")
                st.write("#### {}".format(key))
                st.write("##### {}".format(description))
                st.write("##### Content :")
                placeholders[key] = st.empty()
                st.write("")
                st.write("---")

    if submit_button:
        with st.spinner('Loading data...'):
            if audio_file is not None:
                # upload file and get transcription from whisper
                pass
                # pass transcription to llama
                # pull values from llama output to update case notes and progress notes (update recommended and checkbox if can)
            for key in section_lst:
                print(key)
                placeholders[key].write(f"Hello from {key}")
except Exception as e:
    print(e)