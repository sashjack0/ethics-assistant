# app/ethics_bot.py

"""
Core ethics analysis module for the AI Ethics & Fairness Review Assistant.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from openai.types.chat import ChatCompletion

from app.config.logging_config import setup_logging

# Initialize logging
logger = setup_logging()

# Load environment variables
load_dotenv()

# Initialize OpenAI client with validation
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY is missing in the environment.")
client = OpenAI(api_key=api_key)

def validate_input(project_description: str) -> tuple[bool, Optional[str]]:
    """
    Validate the project description input.
    
    Args:
        project_description: The project description to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not project_description or len(project_description.strip()) < 10:
        return False, "⚠️ Please enter a meaningful project description with at least 10 characters."
    
    if all(char in "!@#$%^&*()_+-=<>?/.,;:'\"[]{}|" for char in project_description.strip()):
        return False, "⚠️ Input appears to contain only symbols. Please provide a meaningful description."
    
    return True, None

def run_ethics_bot(project_description: str) -> Optional[str]:
    """
    Analyze a project description for ethical implications using GPT-3.5.
    
    Args:
        project_description: The project description to analyze
        
    Returns:
        Optional[str]: The ethical analysis response or error message, None if processing fails
    """
    logger.info("Starting ethics analysis for project description")
    
    # Validate input
    is_valid, error_message = validate_input(project_description)
    if not is_valid:
        logger.warning(f"Invalid input: {error_message}")
        return error_message

    try:
        logger.debug("Sending request to OpenAI API")
        response: ChatCompletion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in AI ethics and fairness reviews. When given a project description, assess potential risks around:

- Fairness and bias
- Data privacy
- User consent and transparency
- Legal or regulatory compliance (e.g., GDPR, CCPA)

Respond clearly with numbered points, actionable insights, and a professional tone. Avoid repetition. Be precise but not overly verbose."""
                },
                {"role": "user", "content": project_description}
            ],
            temperature=0.5,
            max_tokens=500,
        )
        
        result = response.choices[0].message.content
        logger.info("Successfully received analysis from OpenAI")
        return result
        
    except (APIError, APIConnectionError, RateLimitError) as e:
        error_msg = f"❌ OpenAI API Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg
