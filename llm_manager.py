import os
from dotenv import load_dotenv
import json

from google import genai

load_dotenv()

api_key_gemini = os.getenv('LLM_API_KEY')
client_gemini = genai.Client(api_key=api_key_gemini)

def reword_question(question, correct_answer, incorrect_answers):
    incorrect_answers_string = ', '.join([f'"{answer}"' for answer in incorrect_answers])
    
    prompt = f'''Reword this quiz question. Change/reword the answers if necessary.
    Question: "{question}". Answer: "{correct_answer}". Incorrect answers: {incorrect_answers_string}.
    Return the reworded question and answers in this JSON format without a code block: 
    {{
        "question": "<value>",
        "correct_answer": "<value>",
        "incorrect_answers": ["<value>", "<value>", "<value>"]
    }}
    . Do not say anything else.
    '''

    try: 
        response = client_gemini.models.generate_content(
            model="gemini-1.5-flash", contents=prompt,
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error: {e}")
        return None

    