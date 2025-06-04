"""
Test suite for the ethics bot functionality.
"""
import pytest
from unittest.mock import MagicMock
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from app.ethics_bot import run_ethics_bot, validate_input
from app.config.logging_config import setup_logging

# Initialize logging
logger = setup_logging()

@pytest.fixture
def sample_descriptions():
    """Fixture providing sample project descriptions for testing."""
    return {
        "loan_model": "We are building a predictive model to flag high-risk loan applicants using their credit history and demographic data.",
        "facial_recognition": "The project involves using facial recognition technology to automate school attendance.",
        "empty": "",
        "health_risk": "Our system predicts likelihood of chronic disease based on health records and wearable device data."
    }

@pytest.fixture
def mock_openai_response():
    """Fixture providing a mock OpenAI API response."""
    return ChatCompletion(
        id="test-id",
        object="chat.completion",
        created=1234567890,
        model="gpt-3.5-turbo",
        choices=[
            Choice(
                index=0,
                message=ChatCompletionMessage(
                    role="assistant",
                    content="1. Fairness and Bias:\n- Consider potential demographic biases in the data\n- Ensure equal treatment across all groups\n\n2. Privacy:\n- Implement data anonymization\n- Follow data protection regulations"
                ),
                finish_reason="stop"
            )
        ]
    )

def test_validate_input(sample_descriptions):
    """Test input validation function."""
    # Test valid input
    is_valid, error = validate_input(sample_descriptions["loan_model"])
    assert is_valid
    assert error is None
    
    # Test empty input
    is_valid, error = validate_input(sample_descriptions["empty"])
    assert not is_valid
    assert "Please enter a meaningful project description" in error
    
    # Test short input
    is_valid, error = validate_input("short")
    assert not is_valid
    assert "Please enter a meaningful project description" in error

def test_ethics_bot_with_mock(mocker, sample_descriptions, mock_openai_response):
    """Test ethics bot with mocked OpenAI API."""
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mocker.patch("app.ethics_bot.client", mock_client)
    
    # Test valid description
    result = run_ethics_bot(sample_descriptions["loan_model"])
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Fairness and Bias" in result
    assert "Privacy" in result
    
    # Verify the mock was called correctly
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "gpt-3.5-turbo"
    assert call_args["temperature"] == 0.5
    assert call_args["max_tokens"] == 500

def test_ethics_bot_error_handling(mocker, sample_descriptions):
    """Test error handling in ethics bot."""
    # Mock the OpenAI client to raise an exception
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mocker.patch("app.ethics_bot.client", mock_client)
    
    # Test error handling
    result = run_ethics_bot(sample_descriptions["loan_model"])
    assert "Error while contacting OpenAI" in result
    assert "API Error" in result

def test_ethics_bot_integration(sample_descriptions):
    """Integration test for the ethics bot."""
    logger.info("Starting integration tests")
    
    # Test valid description
    result = run_ethics_bot(sample_descriptions["loan_model"])
    assert isinstance(result, str)
    assert len(result) > 0
    logger.info("Successfully tested loan model description")
    
    # Test facial recognition case
    result = run_ethics_bot(sample_descriptions["facial_recognition"])
    assert isinstance(result, str)
    assert len(result) > 0
    logger.info("Successfully tested facial recognition description")
    
    # Test empty input
    result = run_ethics_bot(sample_descriptions["empty"])
    assert "Please enter a meaningful project description" in result
    logger.info("Successfully tested empty input handling")
    
    # Test health risk case
    result = run_ethics_bot(sample_descriptions["health_risk"])
    assert isinstance(result, str)
    assert len(result) > 0
    logger.info("Successfully tested health risk description")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
