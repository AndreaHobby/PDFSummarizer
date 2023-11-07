# PDF Summarizer App

A simple Streamlit app that allows users to upload PDF documents, extract text from them, and ask questions to an OpenAI-powered language model for generating answers.

![PDF Summarizer App](https://github.com/AndreaHobby/MaternalHealthLegislationApp/raw/main/MaternalHealthHeader.jpg)


## Table of Contents

- [About this App](#about-this-app)
- [Getting Started](#Getting-Started)
- [Instructions](#instructions)
- [Usage](#usage)
- [References](#references)
- [Disclaimer](#disclaimer)
- [License](#license)

## About this App
This app is designed to analyze text content from uploaded PDF documents. It's powered by OpenAI's GPT-3.5 Turbo language model to answer questions based on the extracted text. The app analyzes the first 8 pages of the document. It can be used for learning exercises and to get answers from textual data.

PDF Text Extraction: The app extracts text content from uploaded PDF documents.
Question & Answer: Users can enter questions related to the extracted text, and the app uses the OpenAI API to generate answers.

## Instructions
Upload your PDF document by clicking the 'Upload PDF' button.
Click the 'Show Extracted Text' button to reveal the extracted text from the uploaded document.
Enter your question in the text input field.
Click the 'Ask' button to get an answer based on the extracted text.

## Getting Started
To run this app locally, you'll need to set up the following:

Install the required Python packages using pip install -r requirements.txt.
Set your OpenAI API key as an environment variable. You can do this by running the following command in your terminal:

export OPENAI_API_KEY=YOUR_API_KEY_HERE

Ensure that you don't include quotes around the API key in the environment variable.

## Usage
Run the app by executing the following command in your terminal:

streamlit run app.py

Access the app in your web browser by following the link provided in the terminal.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
