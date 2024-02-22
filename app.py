# Import necessary libraries
from tempfile import NamedTemporaryFile
import os
import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

# Load environment variables, such as OpenAI API keys
load_dotenv()

# Set Streamlit page configuration with title, icon, and layout settings
st.set_page_config(
    page_title="AI Industrial Designer Resume Feedback Generator",
    page_icon="💯",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Main application title displayed on the page
st.title("AI Industrial Designer Resume Feedback Generator")

# File uploader widget allowing users to upload resumes or cover letters in PDF or DOCX format
uploaded_file = st.file_uploader("Upload a resume / cover letter", type=['pdf', 'docx'])

# Check if a file has been uploaded
if uploaded_file:
    # Read the uploaded file's bytes
    bytes_data = uploaded_file.read()
    # Create a temporary file to save the uploaded file's content
    with NamedTemporaryFile(delete=False) as tmp:  
        tmp.write(bytes_data)  
        # Use PDFReader to process and extract text from the uploaded file
        reader = PDFReader()
        docs = reader.load_data(tmp.name)
        # Initialize OpenAI model with specific instructions tailored for industrial design resume feedback
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
            model="gpt-3.5-turbo",
            temperature=0.0,
            system_prompt="You are a seasoned Industrial Designer with expertise in assessing and improving design portfolios and resumes. [...]",
        )
        # Create a vector store index from the document for processing
        index = VectorStoreIndex.from_documents(docs)
    # Remove the temporary file to clean up
    os.remove(tmp.name)

    # Initialize chat engine if it has not been set in the session state
    if "chat_engine" not in st.session_state.keys():  
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )

    # Trigger initial analysis upon file upload without requiring user interaction
    if "initial_analysis_triggered" not in st.session_state:
        st.session_state.initial_analysis_triggered = True  
        initial_prompt = "Analyze my resume or cover letter file and provide feedback with bullet points."
        st.session_state.messages = [{"role": "user", "content": initial_prompt}]
        # Get feedback from AI based on the uploaded document
        initial_response = st.session_state.chat_engine.stream_chat(initial_prompt)
        if initial_response and initial_response.response:
            # Display the AI-generated feedback to the user
            st.session_state.messages.append({"role": "assistant", "content": initial_response.response})

# Initialize or display a welcome message if no messages exist in the session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome! Please upload your resume or cover letter to start the analysis."}]

# Input widget for users to ask additional questions or request further feedback
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Generate and display response for the new user prompt
    response = st.session_state.chat_engine.stream_chat(prompt)
    if response and response.response:
        st.session_state.messages.append({"role": "assistant", "content": response.response})

# Display all messages (feedback and user queries) in an organized manner
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Check if the last message is not from the assistant and generate a new response if necessary
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add the new assistant message to the session state
