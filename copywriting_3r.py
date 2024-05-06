import google.generativeai as genai
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential


def main():
    set_page_config()
    custom_css()
    hide_elements()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity Copywriting",
        layout="wide",
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


def title_and_description():
    st.title("🧕 Alwrity - AI Generator for The 3 R’s Copywriting Formula")


def input_section():
    with st.expander("**PRO-TIP** - Easy Steps to Create Compelling The 3 R’s Copy", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            st.markdown("**Example Inputs:**")
            st.markdown("Rapport: *'Hey there, fellow fitness enthusiast!'*")
            st.markdown("Reasons: *'Here are three science-backed reasons why our protein powder is the best choice for you.'*")
            st.markdown("Results: *'Experience increased muscle mass, faster recovery, and improved performance in just weeks!'*")
        with col2:
            rapport = st.text_input('**Rapport**', 
                        help="Build a friendly connection with the audience.",
                        placeholder="Find common interests or experiences, Yoga, Tech, Adventure, Fashion...")

            reasons = st.text_input('**Reasons**', 
                        help="Give logical reasons to convince the audience.",
                        placeholder="Save time, money, or effort, safety, comfort...")

            results = st.text_input('**Results**', 
                        help="Describe the benefits the audience will get.",
                        placeholder="Achieve goals, improve quality of life...")

        if st.button('**Get The 3 R’s Copy**'):
	        if rapport.strip() and reasons.strip() and results.strip():
	            with st.spinner("Generating The 3 R’s Copy..."):
	                three_rs_copy = generate_three_rs_copy(rapport, reasons, results)
	                if three_rs_copy:
	                    st.subheader('**👩🔬👩🔬 Your The 3 R’s Copy**')
	                    st.markdown(three_rs_copy)
	                else:
	                    st.error("💥 **Failed to generate The 3 R’s copy. Please try again!**")
	        else:
	            st.error("All fields are required!")
	

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_three_rs_copy(rapport, reasons, results):
    prompt = f"""As an expert copywriter, I need your help in crafting a compelling copy using The 3 R’s (Rapport-Reasons-Results) formula.
        Here's the breakdown:
        - Rapport: {rapport}
        - Reasons: {reasons}
        - Results: {results}
    """
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.6,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

