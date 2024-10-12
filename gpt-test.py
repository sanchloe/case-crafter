import json
import streamlit as st

from src import llama_inference
from tempfile import NamedTemporaryFile
from src.notes_inference import ProgressNotes

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
    audio_file = st.file_uploader("Upload an audio file", type=["mp3"])

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

    transcript = open("transcript_8mins.txt", "r").read()
    progress_notes = ProgressNotes(transcript)  
    json_progress_notes = progress_notes.run_progress_notes()

    client_presentation = json_progress_notes['progress_notes'][0]['client_presentation']
    recommended_text_1 = " ".join([f'<span class="recommendedtext">{item}</span>' for item in client_presentation])
    recommendation_1_placeholder.markdown(f'<p>Recommended: {recommended_text_1}</p>', unsafe_allow_html=True)

    response_to_treatment = json_progress_notes['progress_notes'][0]['response_to_treatment']
    recommended_text_2 = " ".join([f'<span class="recommendedtext">{item}</span>' for item in response_to_treatment])
    recommendation_2_placeholder.markdown(f'<p>Recommended: {recommended_text_2}</p>', unsafe_allow_html=True)

    client_status = json_progress_notes['progress_notes'][0]['client_status']
    recommended_text_3 = " ".join([f'<span class="recommendedtext">{item}</span>' for item in client_status])
    recommendation_3_placeholder.markdown(f'<p>Recommended: {recommended_text_3}</p>', unsafe_allow_html=True)

    risk_assessment = json_progress_notes['progress_notes'][0]['risk_assessment']
    recommended_text_4 = " ".join([f'<span class="recommendedtext">{item}</span>' for item in risk_assessment])
    recommendation_4_placeholder.markdown(f'<p>Recommended: {recommended_text_4}</p>', unsafe_allow_html=True)
    # with section_1[0]:
    #     option_1 = st.checkbox('Anxious')
    #     option_2 = st.checkbox('Confused')
    #     option_3 = st.checkbox('Energetic')
    #     option_4 = st.checkbox('Worried')

    # with section_1[1]:
    #     option_5 = st.checkbox('Fearful')
    #     option_6 = st.checkbox('Cooperative', key="cooperative_1")
    #     option_7 = st.checkbox('Withdrawn')

    # with section_1[2]:
    #     option_8 = st.checkbox('Lethargic')
    #     option_9 = st.checkbox('Relaxed')
    #     option_10 = st.checkbox('Depressed')

    # client_presentation = json_progress_notes['progress_notes'][0]['client_presentation']

    # recommended_text = " ".join([f'<span class="recommendedtext">{item}</span>' for item in client_presentation])

    # # Display the recommendation dynamically in markdown
    # st.markdown(f'<p>Recommended: {recommended_text}</p>', unsafe_allow_html=True)

    # # recommendation_1 = st.markdown('<p>Recommended: <span class="recommendedtext">Anxious</span> <span class="recommendedtext">Fearful</span></p>', unsafe_allow_html=True)

    # st.markdown("###### Response To Treatment")
    # section_2 = st.columns(2)
    # with section_2[0]:
    #     option_11 = st.checkbox('Cooperative', key="cooperative_2")
    #     option_12 = st.checkbox('Uninterested')
    #     option_13 = st.checkbox('Receptive')
    # with section_2[1]:
    #     option_14 = st.checkbox('Combative')
    #     option_15 = st.checkbox('Engaged')

    # recommendation_2 = st.markdown('<p>Recommended: <span class="recommendedtext">Engaged</span> <span class="recommendedtext">Receptive</span></p>', unsafe_allow_html=True)

    # st.markdown("###### Client Status")
    # section_3 = st.columns(2)
    # with section_3[0]:
    #     option_16 = st.checkbox('Improving', key="improving")
    #     option_17 = st.checkbox('Unchanged', key="unchanged")
    # with section_3[1]:
    #     option_18 = st.checkbox('Regressed', key="regressed")
    #     option_19 = st.checkbox('Deteriorating')
    # recommendation_3 = st.markdown('<p>Recommended: <span class="recommendedtext">Unchanged</span></p>', unsafe_allow_html=True)

    # st.markdown("###### Risk Assessment")
    # section_4 = st.columns(2)
    # with section_4[0]:
    #     option_20 = st.checkbox('Attempted to Cause Harm')
    #     option_21 = st.checkbox('Intention to Cause Harm')
    #     option_23 = st.checkbox('Suicidal Ideation')
    # with section_4[1]:
    #     option_24 = st.checkbox('Danger to Self')
    #     option_25 = st.checkbox('Danger to Other')
    #     option_26 = st.checkbox('Plan to Cause Harm')
    # recommendation_4 = st.markdown('<p>Recommended: <span class="recommendedtext">Intention to Cause Harm</span></p>', unsafe_allow_html=True)

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

        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        if len(section_lst) > 0 and len(description_lst) > 0: 
            # Create a bordered section for each section and its description
            l = ['']
            for key, description in zip(section_lst, description_lst):
                l.append(
                    """
                        <h4>{}</h4>
                        <p>{}</p>
                        <p>Content: {}</p>
                        <div id="content-{}"></div>
                    """.format(key, description, text, key))
            st.markdown(
                """
                    <div style="border: 1px solid #BEC6A0; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: white;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2)">
                        {}
                    </div>
                """.format('<br     >'.join(l)), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([3,3,0.5,0.5])
    with col1:
        if st.button(":thumbsup:"):
            print("I have been liked")
    with col2:
        if st.button(":thumbsdown:"):
            print("I have been disliked")
        # Custom CSS to align button to the right
    with col4:
        st.markdown("""
            <style>
            .stButton button {
                float: right;
            }
            </style>
            """, unsafe_allow_html=True)

        if st.button("⚡ Generate"):
            st.write("Button clicked!")