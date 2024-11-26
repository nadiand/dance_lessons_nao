import subprocess
import json

def get_highest_confidence_intent(text):
    """
    Sends a text to the Rasa model and returns the intent with the highest confidence.

    Args:
        text (str): The input text to send to the Rasa model.

    Returns:
        str: The name of the intent with the highest confidence.
    """
    # Define the curl command
    command = [
        'curl', 'localhost:5005/model/parse',
        '--header', 'Content-Type: application/json',
        '--data', f'{{"text": "{text}"}}'
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Access the stdout attribute for the JSON response
    response = result.stdout

    # Parse the JSON string
    parsed_response = json.loads(response)

    # Extract the intent with the highest confidence
    highest_confidence_intent = parsed_response["intent"]["name"]

    return highest_confidence_intent

print(get_highest_confidence_intent("hello"))
