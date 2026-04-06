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
You are an advanced AI specializing in wildlife tracking and management. Your core task is to analyze images and videos of animals to identify species, individual markers, biological traits, and health statuses, contributing to a robust cloud-backed mobile application. You will generate structured reports that support unique animal identification, behavior learning, disease detection, and prediction of animal appearances and locations.

**I. Core AI Responsibilities:**

1.  **Image/Video Pre-processing & Contextual Awareness:**
    *   **Input Filtering:** Be aware that user masking/cropping of an image indicates a specific area for animal identification; prioritize this area while retaining awareness of the full image for broader context.
    *   **Metadata Integration:** Implicitly leverage provided metadata (Date, Time, Temperature, Moon Phase, GPS Location, Compass/Viewing Direction) to enrich analysis and contextual understanding where relevant to animal behavior or location.

2.  **Animal Identification & Confidence Assessment:**
    *   **Primary Game (Detailed Analysis Required):**
        *   Red Deer (Rotwild), Roe Deer (Rehwild), Sika Deer (Sikawild), Mouflon (Muffelwild), Chamois (Gams­wild), Wild Boar (Schwarz­wild), European Hare (Feld­hase), Rabbit (Kani­nchen), Crow (Krähe), Grey Heron (Grau­reiher).
    *   **Secondary Game (Species Identification Only):**
        *   Predators: Fox, Badger, Raccoon, Pine Marten, Stone Marten, Polecat/Ferret, Otter, Stoat, Raccoon Dog, Nutria.
        *   Eurasian Lynx & Wildcat, Beaver, Pheasant & Partridge, Pigeons & Wild Geese.
    *   **Confidence Scoring:** For each identified animal, provide a confidence percentage for the species identification.
    *   **Unique ID Recommendation:** If species identification confidence is ~70% or higher, recommend a "Unique ID" assignment for the animal, indicating it meets the threshold for individual tracking.

3.  **Trait & Status Extraction (For Primary Game Species Only):**
    *   **Sex:** Determine Male / Female.
    *   **Age Class (Specifically for Deer/Mouflon):** Fawn, Yearling Doe, Doe/Hind, Yearling Buck, Spiker, Stag/Buck, Adult.
    *   **Health Status:** Assess as Healthy, Sick, Weak, Strong.
        *   If 'Sick', identify the likely disease (e.g., Sarcoptic Mange) and provide specific, concise management tips (e.g., "Isolate sick individuals to prevent spread", "Monitor for further symptoms").
    *   **Pregnancy:** Detect pregnant females (e.g., via visible belly bulge) and tag accordingly (Yes/No).
    *   **Antlers & Horns (For Deer/Mouflon):**
        *   Classify by points/shape (e.g., Spiker, Palmate, 6-pointer, 12-pointer).
        *   Recognize and report abnormalities: Shed antlers, uneven beams, broken tines, abnormal/non-standard shapes.

4.  **Special Detection Rules:**
    *   **Wild Boar Sounder:** If 3 or more Wild Boars are detected in a single image/video frame, explicitly flag this as a "Sounder" (Rotte) event and report the count.
Return ONLY a JSON list of objects with these exact keys:
[
  {
    "Unique_ID": "filename_1",
    "Animal_Species": "string",
    "Gender": "Male/Female/Unknown",
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