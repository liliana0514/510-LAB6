
# TECHIN 510 Lab 6
Chat with PDF

## Overview
Hi! This is the repository for my AI Industrial Designer Resume Feedback Generator for TECHIN 510.   

## How to Run

Create a gitignore as your first step! Put the following In your gitignore file!
```
.env
/venv
```

Put the following in your requirements.txt file
```
streamlit
openai
llama-index
nltk
pypdf
python-dotenv
```

Open the terminal and run the following commands:
```    
python -m venv venv             
source venv/Scripts/activate        
pip install -r requirements.txt

```

Run the app using the command in the terminal
```bash
streamlit run app.py
```

## Detailed Comment for Every Part
- Load environment variables, such as OpenAI API keys
- Set Streamlit page configuration with title, icon, and layout settings
- File uploader widget allowing users to upload resumes or cover letters in PDF or DOCX format
- Trigger initial analysis upon file upload without requiring user interaction
- Initialize or display a welcome message if no messages exist in the session state
- Check if the last message is not from the assistant and generate a new response if necessary

## Lessons Learned
- Efficient File Handling: The use of temporary files for processing uploaded documents is a secure and efficient way to handle user inputs without risking permanent storage or overuse of memory.
- AI Integration: The integration of AI models for specific tasks (in this case, resume feedback) showcases the flexibility of AI APIs like OpenAI's GPT models in providing tailored assistance.

## Questions / Uncertainties
- Accuracy of AI Feedback: Given the subjective nature of resume and cover letter feedback, how accurate or helpful is the AI-generated advice? This depends significantly on the model's training and the specificity of the prompt.
- Security and Privacy: Uploading personal documents raises questions about data security and privacy. How are uploaded documents and generated feedback handled to ensure user privacy?


## Contact

- Liliana Hsu
# TECHIN510






