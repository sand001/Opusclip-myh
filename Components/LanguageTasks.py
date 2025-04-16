import openai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

# Configuración de la API key
openai.api_key = os.getenv("OPENAI_API")

if not openai.api_key:
    raise ValueError("API key not found. Make sure it is defined in the .env file.")


# Function to extract start and end times
def extract_times(json_string):
    try:
        # Clean the string to ensure valid JSON
        json_string = json_string.strip()
        json_string = re.sub(r'```json\s*|\s*```', '', json_string)
        json_string = re.sub(r'json\s*', '', json_string)
        
        # Parse the JSON string
        data = json.loads(json_string)

        # Extract start and end times as floats
        start_time = float(data[0]["start"])
        end_time = float(data[0]["end"])

        # Convert to integers
        start_time_int = int(start_time)
        end_time_int = int(end_time)
        return start_time_int, end_time_int
    except Exception as e:
        print(f"Error in extract_times: {e}")
        print(f"JSON string received: {json_string}")
        return 0, 0


system = """
Based on the Transcription user provides with start and end, Highlight the main parts in less than 1 min which can be directly converted into a short. Highlight it such that it's interesting and also keep the time stamps for the clip to start and end. Only select a continuous part of the video.

Follow this Format and return in valid JSON:
[{
"start": "Start time of the clip",
"content": "Highlight Text",
"end": "End Time for the highlighted clip"
}]
It should be one continuous clip as it will then be cut from the video and uploaded as a TikTok video. So only have one start, end and content.

Don't say anything else, just return Proper JSON. No explanation etc.
"""

User = """
Any Example
"""


def GetHighlight(Transcription):
    print("Getting Highlight from Transcription ")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": Transcription},
            ],
        )

        json_string = response.choices[0].message.content
        Start, End = extract_times(json_string)
        
        if Start == End:
            print("Error - Trying to get highlights again...")
            Start, End = GetHighlight(Transcription)
            
        return Start, End
    except Exception as e:
        print(f"Error in GetHighlight: {e}")
        return 0, 0


if __name__ == "__main__":
    print(GetHighlight(User))
