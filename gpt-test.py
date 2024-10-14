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
    st.markdown("<h1 style='text-align: center;'>Case Crafter</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Your AI Therapist Ally</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # name section
    st.markdown("""
    <div class="box">
        <div class="row">
            <div class="item"><strong>Client: John Doe</strong></div>
            <div class="item"><strong>Date: 11 October 2024</strong></div>
            <div class="item"><strong>Start Time: 10:00 AM</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([4, 6])

    # Left column (col1) can have multiple items
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

        recommendation_1_placeholder = st.markdown("Recommended:", unsafe_allow_html=True)

        st.markdown("###### Response To Treatment")
        section_2 = st.columns(2)
        with section_2[0]:
            option_11 = st.checkbox('Cooperative', key="cooperative_2")
            option_12 = st.checkbox('Uninterested')
            option_13 = st.checkbox('Receptive')
        with section_2[1]:
            option_14 = st.checkbox('Combative')
            option_15 = st.checkbox('Engaged')

        recommendation_2_placeholder = st.markdown("Recommended:", unsafe_allow_html=True)

        st.markdown("###### Client Status")
        section_3 = st.columns(2)
        with section_3[0]:
            option_16 = st.checkbox('Improving', key="improving")
            option_17 = st.checkbox('Unchanged', key="unchanged")
        with section_3[1]:
            option_18 = st.checkbox('Regressed', key="regressed")
            option_19 = st.checkbox('Deteriorating')

        recommendation_3_placeholder = st.markdown("Recommended:", unsafe_allow_html=True)

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

        recommendation_4_placeholder = st.markdown("Recommended:", unsafe_allow_html=True)

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

        col1, col2, col3, col4 = st.columns([1, 1, 6, 1])  # Adjusted column widths
        #TODO: fix button layout
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

        # Custom CSS to align button to the right
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
                        # audio_transcription = utils.read_transcript("./src/dependencies/sample_transcript_8mins.txt")
                        # -----------

                        # pass transcription to llama
                        user_template_option = user_template_option.lower()
                        # get case notes output
                        notes_template = utils.load_template(f"./src/dependencies/{user_template_option}")
                        notes_generator = CaseNotesGenerator(transcript, notes_template)
                        case_notes = notes_generator.get_notes()

                        # get progress notes output
                        progress_notes = ProgressNotes(transcript)
                        json_progress_notes = progress_notes.run_progress_notes()

                        # update case notes
                        content_lst = []
                        for key, value in case_notes.items():
                            content_lst.append(value)
                        for i in range(len(content_lst)):
                            st.session_state['content_text'][i] = f"{content_lst[i]}"
                        section_placeholder.markdown(render_sections(section_lst, description_lst, st.session_state['content_text']), unsafe_allow_html=True)

                        # update progress notes
                        client_presentation = json_progress_notes['progress_notes'][0]['client_presentation']
                        update_recommendations(recommendation_1_placeholder, client_presentation, "Recommended")

                        response_to_treatment = json_progress_notes['progress_notes'][0]['response_to_treatment']
                        update_recommendations(recommendation_2_placeholder, response_to_treatment, "Recommended")

                        client_status = json_progress_notes['progress_notes'][0]['client_status']
                        update_recommendations(recommendation_3_placeholder, client_status, "Recommended")

                        risk_assessment = json_progress_notes['progress_notes'][0]['risk_assessment']
                        update_recommendations(recommendation_4_placeholder, risk_assessment, "Recommended")

except Exception as e:
    print(traceback.format_exc())