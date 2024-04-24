# Alwrity - AI Generator for The 3 R’s Copywriting Formula

Alwrity is an AI-powered generator designed to assist users in creating compelling marketing copy using the 3 R’s (Rapport-Reasons-Results) copywriting formula. This tool leverages OpenAI's powerful ChatGPT model to generate copy based on user-provided inputs.

## Features

- **Input Section:** Users can input rapport, reasons, and results to generate copy.
- **Pro-Tip:** Provides guidance on how to use the 3 R’s copywriting formula effectively.
- **Progress Spinner:** Displays a spinner during copy generation.
- **Error Handling:** Handles exceptions gracefully and provides helpful error messages.

## How to Use

1. **Input Section:** Enter the rapport, reasons, and results in the input fields provided.
2. **Generate Copy:** Click the "Get The 3 R’s Copy" button to generate copy based on the provided inputs.
3. **View Copy:** Once generated, the copy will be displayed in the web app for review and use.

## Requirements

- Python 3.6+
- Streamlit
- Tenacity
- OpenAI
- Streamlit Lottie

## How to Run

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up environment variables:
   - `OPENAI_API_KEY`: OpenAI API key.
4. Run the Alwrity script using `streamlit run alwrity.py`.
