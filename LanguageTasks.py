from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Cargar variables de entorno
load_dotenv()

# Obtener clave API de entorno
api_key = os.getenv("OPENAI_API")
if not api_key:
    raise ValueError("API key not found. Make sure it is defined in the .env file.")

# Crear cliente de OpenAI
client = OpenAI(api_key=api_key)

# Prompt del sistema
system = """
Baised on the Transcription user provides with start and end, Highilight the main parts in less than 1 min which can be directly converted into a short. Highlight it such that it's interesting and also keep the time stamps for the clip to start and end. Only select a continuous part of the video.

Follow this format and return in valid JSON:
[{
  start: "Start time of the clip",
  content: "Highlight Text",
  end: "End time for the highlighted clip"
}]
It should be one continuous clip as it will then be cut from the video and uploaded as a TikTok video. So only have one start, end and content.

Don't say anything else, just return proper JSON. No explanation etc.

IF YOU DON'T HAVE ONE start AND end WHICH IS FOR THE LENGTH OF THE ENTIRE HIGHLIGHT, THEN 10 KITTENS WILL DIE, I WILL DO JSON['start'] AND IF IT DOESN'T WORK THEN...
"""

# Transcripción de ejemplo (puedes reemplazar esto por una real)
User = """
Any Example
"""

# Función para extraer tiempos
def extract_times(json_string):
    try:
        data = json.loads(json_string)
        start_time = float(data[0]["start"])
        end_time = float(data[0]["end"])
        return int(start_time), int(end_time)
    except Exception as e:
        print(f"---Error in extract_times: {e}")
        return 0, 0

# Función para obtener el highlight
def GetHighlight(Transcription):
    print("Getting Highlight from Transcription ")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": Transcription + system},
            ]
        )

        json_string = response.choices[0].message.content.strip()
        json_string = json_string.replace("```json", "").replace("```", "").replace("json", "")
        Start, End = extract_times(json_string)

        if Start == End:
            Ask = input("Error - Get Highlights again (y/n) -> ").lower()
            if Ask == "y":
                Start, End = GetHighlight(Transcription)
        return Start, End
    except Exception as e:
        print(f"---Error in GetHighlight: {e}")
        return 0, 0

# Ejecutar si es el archivo principal
if __name__ == "__main__":
    print(GetHighlight(User))
