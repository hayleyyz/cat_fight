import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY not found in .env file. Please set it.")
client = anthropic.Anthropic(api_key=api_key)

def generate_fighter_profile(base64_frames: list[str]) -> dict:
    """
    Generates a cat fighter profile by sending video frames to the Claude 3.5 Sonnet API.

    Args:
        base64_frames: A list of base64-encoded JPEG image strings. For this V2,
                       it will typically be a list with just one cropped portrait.

    Returns:
        A dictionary containing the parsed JSON data for the fighter profile.

    Raises:
        ValueError: If the API returns an error.
    """
    system_prompt = """
    You are a fighting game announcer and character creator. Your task is to analyze the provided
    image of a cat and generate a "fighter profile" inspired by games like Street Fighter
    or Super Smash Bros. The cat is the fighter. Analyze its appearance, perceived actions, and
    environment to assign it a creative name, stats, and a personality.

    Your response MUST be a single, valid JSON object with the following keys:
    - "name": A cool, pun-based, or epic-sounding fighter name (e.g., "Whisker Fury", "Clawdia Scratch").
    - "attack": A number between 0 and 100 representing perceived offensive power.
    - "defense": A number between 0 and 100 representing perceived defensive capability (e.g., fluffiness, hiding).
    - "speed": A number between 0 and 100 based on perceived movement or agility.
    - "agility": A number between 0 and 100 based on perceived nimbleness or dexterity.
    - "special_move": A creative name for a signature fighting move (e.g., "Hairball Hurricane", "Pounce of Fury").
    - "personality": A brief, 2-3 word description of the cat's fighting temperament (e.g., "Mischievous but tactical").
    - "catchphrase": A short, punchy quote the cat might say before a fight (e.g., "You thought I was napping?").

    Do not include any text, explanations, or markdown formatting outside of the JSON object itself.
    """

    messages = [
        {
            "role": "user",
            "content": [
                *[{
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": frame,
                    },
                } for frame in base64_frames],
                {
                    "type": "text",
                    "text": "Analyze this cat and generate its fighter profile."
                }
            ],
        }
    ]

    try:
        print("Sending one portrait to Claude API...")
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            system=system_prompt,
            messages=messages,
        )
        
        response_text = response.content[0].text
        cleaned_json = response_text.strip().removeprefix("```json").removesuffix("```")
        
        profile_data = json.loads(cleaned_json)
        return profile_data

    except Exception as e:
        print(f"An error occurred while communicating with the Claude API: {e}")
        raise ValueError(f"API Error: {e}")
