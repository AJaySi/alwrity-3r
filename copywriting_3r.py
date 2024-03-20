import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
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

def sidebar():
    st.sidebar.title("The 3 R’s Copywriting Formula")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for The 3 R’s Copywriting Formula")
    with st.expander("What is **The 3 R’s Copywriting Formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's The 3 R’s Copywriting Formula, and How to use this AI generator 🗣️
            ---
            #### The 3 R’s Copywriting Formula

            The 3 R’s stands for Rapport-Reasons-Results. It's a copywriting framework that focuses on guiding the audience through different stages:

            1. **Rapport**: Establishing a connection or bond with the audience.
            2. **Reasons**: Providing logical reasons or justifications for taking action.
            3. **Results**: Highlighting the potential outcomes or benefits of taking action.

            The 3 R’s formula helps in building trust, credibility, and persuasion in copywriting.

            #### The 3 R’s Copywriting Formula: Simple Example

            - **Rapport**: "Hey there, fellow fitness enthusiast!"
            - **Reasons**: "Here are three science-backed reasons why our protein powder is the best choice for you."
            - **Results**: "Experience increased muscle mass, faster recovery, and improved performance in just weeks!"

            ---
        ''')


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
	
    page_bottom()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_three_rs_copy(rapport, reasons, results):
    prompt = f"""As an expert copywriter, I need your help in crafting a compelling copy using The 3 R’s (Rapport-Reasons-Results) formula.
        Here's the breakdown:
        - Rapport: {rapport}
        - Reasons: {reasons}
        - Results: {results}
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """Display the bottom section of the web app."""
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using The 3 R’s Copywriting Formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Example Copy:
    - Rapport: *'Hey there, fellow fitness enthusiast!'*
    - Reasons: *'Here are three science-backed reasons why our protein powder is the best choice for you.'*
    - Results: *'Experience increased muscle mass, faster recovery, and improved performance in just weeks!'*
    """)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=1):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()

