import fitz  # PyMuPDF
import openai
import os
import streamlit as st
import tempfile
from PIL import Image
from io import BytesIO
import time  # Import the time module

# Set Your API Key as an Environment Variable:
# In your terminal, set your OpenAI API key as an environment variable.
# You can do this by running the following command (replace YOUR_API_KEY_HERE with your actual OpenAI API key):
# export OPENAI_API_KEY=YOUR_API_KEY_HERE
# Ensure that you don't include quotes around the API key in the environment variable. This is really important because the app will not work if this is not done.

st.set_page_config(layout='wide', page_title='PDF Summarizer App', page_icon="img/hdslogo.PNG")

# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

@st.cache_data
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

# Function to ask a question using OpenAI's API
@st.cache_data
def ask_openai_question(text, question, openai_api_key, max_tokens=150):
    openai.api_key = openai_api_key
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Document: {text}\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens, # Adjust the max_tokens as needed
            stop=["\n"]
        )
        answer = response.choices[0].text.strip()
        # Introduce a pause to handle rate limits
        time.sleep(1)  # Adjust the sleep duration as needed
        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app
def main():

    # Add a header image
    header_image = Image.open("HeaderT.png")
    st.image(header_image, use_column_width=True)

    extracted_text = ""
    # Add custom CSS styles to change the background color to purple
    st.markdown(
        """
        <style>
        body {
            background-color: purple;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # App Summary
    st.markdown("## About this App:")
    st.markdown("This app will analyze texts that you upload."
                "This app only analyzes 8 pages of the document at a time as this was done for a learning exercise.")
    st.markdown(
        "A large language model from OpenAI was used to create this app, which is still evolving, so answers may appear different over time.")

    # Add instructions
    st.markdown("## Instructions:")
    st.markdown("1. Upload your PDF document by clicking the 'Upload PDF' button.")
    st.markdown("2. Click the 'Show Extracted Text' button to reveal the extracted text from the uploaded document.")
    st.markdown("3. Enter your question in the text input field.")
    st.markdown("4. Click the 'Ask' button to get an answer based on the extracted text.")

    # File uploader for the PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        

        # Check if the PDF has more than 8 pages
        with fitz.open(temp_file_path) as pdf:
            page_count = len(pdf)
            if page_count > 8:
                st.warning(
                    "The uploaded PDF has more than 8 pages. It will be split into chunks of 8 pages for analysis.")
                num_chunks = (page_count - 1) // 8 + 1

                for chunk_number in range(num_chunks):
                    st.write(f"Chunk {chunk_number + 1} of {num_chunks}:")
                    chunk_start = chunk_number * 8
                    chunk_end = min(chunk_start + 8, page_count)
                    st.write(f"Analyzing pages {chunk_start + 1} to {chunk_end}...")

                    # Extract text from this chunk of pages
                    chunk_text = extract_text_from_pdf(temp_file_path)
                    chunk_text = '\n'.join(chunk_text.split('\n')[chunk_start * 8:chunk_end * 8])

                    # Add a unique key for the "Show Extracted Text" button
                    show_text = st.button(f"Show Extracted Text (Chunk {chunk_number + 1})",
                                          key=f"show_text_{chunk_number}")

                    if show_text:
                        st.header("Extracted Text from Uploaded PDF")
                        st.text(chunk_text)

                    st.markdown(f"#### Have a question for Chunk {chunk_number + 1}?")
                    # Add a unique key for the text input field
                    question = st.text_input(f"## Enter your question here (Chunk {chunk_number + 1}):",
                                             key=f"question_{chunk_number}")

                    # Add a unique key for the "Ask" button
                    if st.button(f"Ask (Chunk {chunk_number + 1})", key=f"ask_button_{chunk_number}"):
                        if question:
                            openai_api_key = os.getenv("OPENAI_API_KEY")
                            answer = ask_openai_question(chunk_text, question, openai_api_key)
                            st.header("Answer:")
                            st.write(answer)
                        else:
                            st.warning("Please enter a question.")



    else:
        st.warning("Please upload a valid PDF file.")

if __name__ == "__main__":
    main()
