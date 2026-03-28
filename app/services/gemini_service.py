import google.generativeai as genai
import json
import time
import os
import google.generativeai as genai
from app.core.config import settings

# ✅ Use config instead of hardcoding
genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

PROMPT = """
Analyze this trail camera image for wildlife monitoring. 
If multiple animals are present, identify each one separately.
Return ONLY a JSON list of objects with these exact keys:
[
  {
    "Unique_ID": "filename_1",
    "Animal_Species": "string",
    "Gender": "Male/Female/Unknown",
    "Confidence": "High/Medium/Low",
    "Age": "Adult/Juvenile/Piglet/Unknown",
    "Health_Status": "Healthy/Injured/Sick",
    "Observations": "Brief description"
  }
]
If no animal is present, return a list with one object where Species is 'None'.
"""

def analyze_image(image_path: str):
    filename = os.path.basename(image_path)
    results = []

    try:
        file = genai.upload_file(path=image_path)
        response = model.generate_content([file, PROMPT])

        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        data_list = json.loads(raw_text)

        for i, animal in enumerate(data_list):
            animal["Unique_ID"] = f"{filename}_{i+1}"
            results.append(animal)

        time.sleep(2)

    except Exception as e:
        results.append({
            "Unique_ID": filename,
            "Animal_Species": "Error",
            "Gender": "Unknown",
            "Age": "Unknown",
            "Health_Status": "Unknown",
            "Observations": str(e)
        })

    return results