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

st.set_page_config(layout='wide', page_title='PDF Summarizer App')

@st.cache_data
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

# Function to ask a question using OpenAI's API
@st.cache_data
def ask_openai_question(text, question, openai_api_key):
    openai.api_key = openai_api_key
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Document: {text}\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=100,
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
                "This app only analyzes the  8 pages of the document at a time as this was done for a learning exercise.")
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
                st.error("Error: The uploaded PDF has more than 8 pages. This app only analyzes the first 8 pages.")
            else:
                extracted_text = extract_text_from_pdf(temp_file_path)
                show_text = st.button("Show Extracted Text")
                if show_text:
                    st.header("Extracted Text from Uploaded PDF")
                    st.text(extracted_text)

                st.markdown("#### Have a question?")
                question = st.text_input("## Enter your question here:")

                if st.button("Ask"):
                    if question:
                        openai_api_key = os.getenv("OPENAI_API_KEY")
                        answer = ask_openai_question(extracted_text, question, openai_api_key)
                        st.header("Answer:")
                        st.write(answer)
                    else:
                        st.warning("Please enter a question.")

                for page in pdf:
                    img = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                    img_bytes = img.tobytes()
                    img = Image.open(BytesIO(img_bytes))
                    st.image(img)

    else:
        st.warning("Please upload a valid PDF file.")

if __name__ == "__main__":
    main()
