import os
import json
import whisper
import traceback
import streamlit as st

from src import utils
from src.db_handler import DBConnector
from src.speech_inference import SpeechToText
from src.notes_inference import ProgressNotes
from src.llama_inference import CaseNotesGenerator

st.set_page_config(page_title="Case Crafter",layout="wide")

template_dict = {
    "SOAP": "soap.json",
    "DAP": "dap.json",
    "BIRP": "birp.json"
}

utils.load_css('./src/css_styles/style.css')
whisper_model = whisper.load_model("base")

db_connector = DBConnector()
session_id, therapist_id, client_id, client_name = utils.setup_session()
if "session_id" not in st.session_state: 
    st.session_state["session_id"] = session_id
else:
    session_id = st.session_state["session_id"]

def render_sections(section_lst, description_lst, content_lst):
    l = ['']
    for idx, (key, description) in enumerate(zip(section_lst, description_lst)):
        content = content_lst[idx]
        l.append(
            """
                <h4>{}</h4>
                <p>{}</p>
                <p>Content: {}</p>
            """.format(key, description, content)
        )
    return """
        <div style="border: 1px solid #BEC6A0; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: white;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2)">
            {}
        </div>
    """.format('<br>'.join(l))

def update_recommendations(placeholder, category_data, label):
    if len(category_data) > 0:
        recommended_text = " ".join([f'<span class="recommendedtext">{item}</span>' for item in category_data])
        placeholder.markdown(f'<p>{label}: {recommended_text}</p>', unsafe_allow_html=True)
    else:
        placeholder.markdown(f'<p>{label}: None</p>', unsafe_allow_html=True)

try:

    db_connector.connect()

    st.markdown("<h1 style='text-align: center;'>Case Crafter</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Your AI Therapist Ally</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # name section
    st.markdown(f"""
    <div class="box">
        <div class="row">
            <div class="item"><strong>Client: {client_name}</strong></div>
            <div class="item"><strong>Date: 17 October 2024</strong></div>
            <div class="item"><strong>Start Time: 10:00 AM</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([4, 6])

     # Initialize session state for recommendation text
    if 'client_presentation' not in st.session_state:
        st.session_state['client_presentation'] = '<p>Recommended: </p>'
    if 'response_to_treatment' not in st.session_state:
        st.session_state['response_to_treatment'] = '<p>Recommended: </p>'
    if 'client_status' not in st.session_state:
        st.session_state['client_status'] = '<p>Recommended: </p>'
    if 'risk_assessment' not in st.session_state:
        st.session_state['risk_assessment'] = '<p>Recommended: </p>'

    with left_col:
        st.markdown('')
        st.markdown("##### Upload Audio")
        audio_file = st.file_uploader("Upload Audio", type=["mp3", "mp4", "wav", "m4a"])
        if audio_file:
            utils.save_audio_file(audio_file.read(), "mp3")

        st.markdown("##### Template Style")
        user_template_option = st.selectbox('Select your preferred template style',('SOAP', 'DAP', 'BIRP'))
        st.write('You selected:', user_template_option)

        st.markdown("#### Progress Notes")

        st.markdown("###### Client Presentation")
        section_1 = st.columns(3)
        with section_1[0]:
            option_1 = st.checkbox('Anxious')
            option_2 = st.checkbox('Confused')
            option_3 = st.checkbox('Energetic')
            option_4 = st.checkbox('Worried')
        with section_1[1]:
            option_5 = st.checkbox('Fearful')
            option_6 = st.checkbox('Cooperative', key="cooperative_1")
            option_7 = st.checkbox('Withdrawn')
        with section_1[2]:
            option_8 = st.checkbox('Lethargic')
            option_9 = st.checkbox('Relaxed')
            option_10 = st.checkbox('Depressed')

        recommendation_1_placeholder = st.empty()
        recommendation_1_placeholder.markdown(st.session_state['client_presentation'], unsafe_allow_html=True)

        st.markdown("###### Response To Treatment")
        section_2 = st.columns(2)
        with section_2[0]:
            option_11 = st.checkbox('Cooperative', key="cooperative_2")
            option_12 = st.checkbox('Uninterested')
            option_13 = st.checkbox('Receptive')
        with section_2[1]:
            option_14 = st.checkbox('Combative')
            option_15 = st.checkbox('Engaged')

        recommendation_2_placeholder = st.empty()
        recommendation_2_placeholder.markdown(st.session_state['response_to_treatment'], unsafe_allow_html=True)

        st.markdown("###### Client Status")
        section_3 = st.columns(2)
        with section_3[0]:
            option_16 = st.checkbox('Improving', key="improving")
            option_17 = st.checkbox('Unchanged', key="unchanged")
        with section_3[1]:
            option_18 = st.checkbox('Regressed', key="regressed")
            option_19 = st.checkbox('Deteriorating')

        recommendation_3_placeholder = st.empty()
        recommendation_3_placeholder.markdown(st.session_state['client_status'], unsafe_allow_html=True)

        st.markdown("###### Risk Assessment")
        section_4 = st.columns(2)
        with section_4[0]:
            option_20 = st.checkbox('Attempted to Cause Harm')
            option_21 = st.checkbox('Intention to Cause Harm')
            option_23 = st.checkbox('Suicidal Ideation')
        with section_4[1]:
            option_24 = st.checkbox('Danger to Self')
            option_25 = st.checkbox('Danger to Other')
            option_26 = st.checkbox('Plan to Cause Harm')

        recommendation_4_placeholder = st.empty()
        recommendation_4_placeholder.markdown(st.session_state['risk_assessment'], unsafe_allow_html=True)

    with right_col:
        # Output column
        with st.container():
            section_lst = []
            description_lst = []
            content_lst= []
            st.markdown("#### Case Notes")

            if user_template_option in template_dict:
                json_template_file = template_dict[user_template_option]
            json_file = "./src/dependencies/{}".format(json_template_file)
            with open(json_file, 'r') as file:
                data = json.load(file)
                for section, details in data['sections'].items():
                    section_lst.append(section)
                    description_lst.append(details['description'])
                    content_lst.append(details["content"])
            placeholders = {}

            if 'content_text' not in st.session_state:
                st.session_state['content_text'] = [""] * len(section_lst)  # Empty content initially for all sections

            # Placeholder for bordered section
            section_placeholder = st.empty()
            section_placeholder.markdown(render_sections(section_lst, description_lst, st.session_state['content_text']), unsafe_allow_html=True)

        if 'disliked' not in st.session_state:
            st.session_state['disliked'] = False
        col1, col2, col3, col4 = st.columns([1, 1, 4, 1.5])

        with col1:
            st.markdown(
                """
                <style>
                .stButton button {
                    margin-left: 0;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            if st.button(":thumbsup:"):
                st.session_state['disliked'] = False
                print("I have been liked")

        with col2:
            st.markdown(
                """
                <style>
                .stButton button {
                    margin-left: 0;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            if st.button(":thumbsdown:"):
                print("I have been disliked")
                st.session_state['disliked'] = True

        if st.session_state['disliked']:
            feedback_options = ['Too Long', 'Not accurate', 'Not relevant', 'Too verbose', 'Poor tone or style', 'Biased or inappropriate', 'Confusing or Unclear', 'Other']
            user_feedback = st.selectbox("Please tell us why you disliked it:", feedback_options)

            if user_feedback:
                st.write(f"You selected: {user_feedback}")

            if user_feedback == 'Other':
                text_col1, save_col2 = st.columns([4, 1])

                with text_col1:
                    user_custom_feedback = st.text_input("Please provide more details")

                # Save button
                with save_col2:
                    st.write("")
                    save_button = st.button("💾 Save")

        with col4:
            st.markdown(
                    """
                    <style>
                    .stButton button {
                        float: right;
                        width: 100%;  /* Take full width */
                        white-space: nowrap;  /* Prevent breaking */
                        padding: 10px;  /* Add padding for spacing */
                        overflow: hidden;  /* Ensure no text overflows */
                        text-overflow: ellipsis;  /* Add ellipsis if text is too long */
                        font-size: 16px;  /* Adjust font size */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            if st.button("⚡ Generate"):

                print("Generate clicked")
                with st.spinner("Loading Data..."):
                    if audio_file is not None:
                        #Run whisper model
                        audio_file = max(
                            [f for f in os.listdir(".") if f.startswith("audio")],
                            key=os.path.getctime,
                        )
                        print('TOYCH', audio_file)
                        get_transcript = SpeechToText(audio_file)
                        transcript = get_transcript.transcribe_audio(whisper_model)
                        print(transcript)

                        # TO DELETE ------
                        # transcript = utils.read_transcript("./src/dependencies/sample_transcript_8mins.txt")
                        # -----------

                        # pass transcription to llama
                        user_template_option = user_template_option.lower()
                        # get case notes output
                        notes_template = utils.load_template(f"./src/dependencies/{user_template_option}")
                        notes_generator = CaseNotesGenerator(transcript, notes_template)
                        case_notes = notes_generator.get_notes()

                        #push case notes to db
                        db_connector.insert_case_notes(session_id, client_id, client_name, therapist_id, str(case_notes))

                        # get progress notes output
                        progress_notes = ProgressNotes(transcript)
                        json_progress_notes = progress_notes.run_progress_notes()

                        #push progress notes to db here

                        # update case notes
                        content_lst = []
                        for key, value in case_notes.items():
                            content_lst.append(value)
                        for i in range(len(content_lst)):
                            st.session_state['content_text'][i] = f"{content_lst[i]}"
                        section_placeholder.markdown(render_sections(section_lst, description_lst, st.session_state['content_text']), unsafe_allow_html=True)

                        # update progress notes
                        client_presentation = json_progress_notes['progress_notes'][0]['client_presentation']
                        response_to_treatment = json_progress_notes['progress_notes'][0]['response_to_treatment']
                        client_status = json_progress_notes['progress_notes'][0]['client_status']
                        risk_assessment = json_progress_notes['progress_notes'][0]['risk_assessment']

                        client_presentation_html = '<p>Recommended: ' + ' '.join([f'<span class="recommendedtext">{item}</span>' for item in client_presentation]) + '</p>'
                        response_to_treatment_html = '<p>Recommended: ' + ' '.join([f'<span class="recommendedtext">{item}</span>' for item in response_to_treatment]) + '</p>'
                        client_status_html = '<p>Recommended: ' + ' '.join([f'<span class="recommendedtext">{item}</span>' for item in client_status]) + '</p>'
                        risk_assessment_html = '<p>Recommended: ' + ' '.join([f'<span class="recommendedtext">{item}</span>' for item in risk_assessment]) + '</p>'

                        # Update session state
                        st.session_state['client_presentation'] = client_presentation_html
                        st.session_state['response_to_treatment'] = response_to_treatment_html
                        st.session_state['client_status'] = client_status_html
                        st.session_state['risk_assessment'] = risk_assessment_html

                        # Update the placeholders with the new recommendations using HTML
                        update_recommendations(recommendation_1_placeholder, client_presentation, "Recommended")
                        update_recommendations(recommendation_2_placeholder, response_to_treatment, "Recommended")
                        update_recommendations(recommendation_3_placeholder, client_status, "Recommended")
                        update_recommendations(recommendation_4_placeholder, risk_assessment, "Recommended")

            if save_button:
                db_connector.update_feedback(session_id, user_custom_feedback)

    db_connector.close()

except Exception as e:
    print(traceback.format_exc())