from google import genai
import os
from dotenv import load_dotenv

# .env file load karne ke liye
load_dotenv()

def ask_ai(user_input):
    try:
        # API Key uthao
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "Error: API Key nahi mili. Check .env file."

        # Naya Client Initialize karo (Latest Method)
        client = genai.Client(api_key=api_key)

        # Content generate karo
        response = client.models.generate_content(
            model="gemini-flash-latest",
            # model="gemini-pro-latest",
            contents=user_input
        )
        
        return response.text

    except Exception as e:
        return f"Error aa gaya bhai: {e}"