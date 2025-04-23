# app/ethics_bot.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client (v1.x compatible)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_ethics_bot(project_description):
    # Basic input validation
    if not project_description or len(project_description.strip()) < 10:
        return "⚠️ Please enter a meaningful project description with at least 10 characters."
    if all(char in "!@#$%^&*()_+-=<>?/.,;:'\"[]{}|" for char in project_description.strip()):
        return "⚠️ Input appears to contain only symbols. Please provide a meaningful description."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in AI ethics and fairness reviews. When given a project description, assess potential risks around:\n\n- Fairness and bias\n- Data privacy\n- User consent and transparency\n- Legal or regulatory compliance (e.g., GDPR, CCPA)\n\nRespond clearly with numbered points, actionable insights, and a professional tone. Avoid repetition. Be precise but not overly verbose."},
                {"role": "user", "content": project_description}
            ],
            temperature=0.5,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error while contacting OpenAI: {str(e)}"
