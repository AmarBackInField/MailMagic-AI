from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
load_dotenv()
# Google API Key
Google_api_key = os.getenv("Google_api_key")

# Initialize the AI model
model = ChatGoogleGenerativeAI(api_key=Google_api_key, model="gemini-2.0-flash-lite")

# Define the prompt template
prompt_template = """
You are a professional expert in crafting compelling Gmail email bodies based on the user's resume and job description.

### Instructions:
- Given the following query: **"{query}"**, generate the best possible email body.
- Don't generate irrelvant text as it should be looks like that human write this.
- The user has a default experience of 2.5 years unless specified otherwise in the query.
- Use information directly from the resume text provided below.
- Highlight the user's relevant experience and skills that match the job description.
- If no relevant data is found, return a well-structured but generic default email body.
- Use HTML tags for formatting, such as <b> for bold text.
- Don't use irrelevant and extra texts.

### Resume Text:
{resume_text}

### Example Query:
"Apply for the position of Software Engineer at XYZ Company. Highlight my experience with Python and machine learning."

### Email Body:
<p>Dear Hiring Manager,</p>

<p>I am writing to express my interest in the Software Engineer position at <b>XYZ Company</b>, as advertised. With over 2.5 years of experience in software development, I am confident in my ability to contribute effectively to your team.</p>

<p>In my previous role at <b>ABC Corporation</b>, I developed and maintained various software applications using Python. I have a strong background in machine learning and have successfully implemented several machine learning models that improved our product's performance. My skills include:</p>

<ul>
  <li>Proficient in Python programming.</li>
  <li>Experience with machine learning frameworks such as TensorFlow and scikit-learn.</li>
  <li>Strong problem-solving skills and attention to detail.</li>
  <li>Ability to work collaboratively in a team environment.</li>
</ul>

<p>I am particularly drawn to <b>XYZ Company</b> because of your innovative approach to technology and your commitment to excellence. I am eager to bring my skills and experience to your team and contribute to your ongoing success.</p>

<p>Thank you for considering my application. I look forward to the opportunity to discuss how my background, skills, and certifications align with the needs of your team.</p>

<p>Sincerely,</p>
<p>[Your Name]</p>
<p>[Contact Details]</p>
"""


prompt = ChatPromptTemplate.from_template(prompt_template)

# Create the chain
chain = prompt | model | StrOutputParser()

# Define the prompt for Chain 2
# from langchain.prompts import ChatPromptTemplate

prompt2 = ChatPromptTemplate.from_template(
    """You are a professional at filling in email templates. Given the following template:
    {template_content}
    and the user's resume information:
    {resume_text}
    Fill in the missing details appropriately to create a professional email. Ensure the email is free from any unwanted words, symbols, or HTML tags. The email should be clear, concise, and professionally written."""
)

chain2 = prompt2 | model | StrOutputParser()

# Function to extract text from a resume PDF
def extract_resume_text(file_path):
    """Extract text from PDF resume"""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip()
    except Exception as e:
        return ""
