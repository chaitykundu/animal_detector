import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-lite"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# -----------------------------
# ANALYSIS FUNCTION
# -----------------------------
def analyze_file(file_path, file_type="Video"):
    if not os.path.exists(file_path):
        print(f"{file_type} file not found: {file_path}")
        return None

    try:
        print(f"Uploading {file_type.lower()}: {file_path}")
        uploaded_file = genai.upload_file(path=file_path)
        time.sleep(10 if file_type == "Image" else 20)  # wait for processing
        uploaded_file = genai.get_file(uploaded_file.name)

        prompt = f"""
Analyze this wildlife {file_type.lower()}.

Provide ONE overall result for the whole {file_type.lower()}.

Focus on:
- species
- gender
- age
- health (include disease & management if sick)
- pregnancy
- antlers/horns (if present)
- behavior

Return **valid JSON only** with this structure:

{{
  "Animal_ID": "{os.path.basename(file_path)}",
  "Species": "string",
  "Gender": "Male/Female/Unknown",
  "Age": "Adult/Juvenile/Unknown",
  "Health_Status": {{
      "Condition": "Healthy/Injured/Sick/Unknown",
      "Likely_Disease": "string or N/A",
      "Management_Tips": "string or N/A"
  }},
  "Pregnancy_Status": "Yes/No/Unknown",
  "Antlers_Horns": {{
      "Type": "string or N/A",
      "Condition": "string or N/A",
      "Notes": "string or N/A"
  }},
  "Observations": raw_text
}}
"""
        response = model.generate_content([uploaded_file, prompt])
        raw_text = response.text.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(raw_text)
            # Ensure all keys exist
            data.setdefault("Health_Status", {"Condition": "Unknown", "Likely_Disease": "N/A", "Management_Tips": "N/A"})
            data.setdefault("Pregnancy_Status", "Unknown")
            data.setdefault("Antlers_Horns", {"Type": "N/A", "Condition": "N/A", "Notes": ""})
            data.setdefault("Observations", "")
            return data
        except json.JSONDecodeError:
            return {
                "Animal_ID": os.path.basename(file_path),
                "Species": "Unknown",
                "Gender": "Unknown",
                "Age": "Unknown",
                "Health_Status": {"Condition": "Unknown", "Likely_Disease": "N/A", "Management_Tips": "N/A"},
                "Pregnancy_Status": "Unknown",
                "Antlers_Horns": {"Type": "N/A", "Condition": "N/A", "Notes": ""},
                "Observations": raw_text
            }

    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None

# -----------------------------
# FOLDER BATCH PROCESSING
# -----------------------------
def analyze_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    all_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.jpg', '.jpeg', '.png', '.bmp'))
    ]

    if not all_files:
        print("No video or image files found in the folder.")
        return

    results = []

    for idx, file_path in enumerate(all_files, 1):
        file_ext = os.path.splitext(file_path)[1].lower()
        file_type = "Image" if file_ext in ('.jpg', '.jpeg', '.png', '.bmp') else "Video"
        print(f"\nProcessing {idx}/{len(all_files)}: {file_path} ({file_type})")
        result = analyze_file(file_path, file_type=file_type)
        if result:
            results.append(result)

    output_file = os.path.join(folder_path, "analysis_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nAll results saved to: {output_file}")

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    folder_path = r"C:\Users\Chaity Kundu\Desktop\Chaity\animal\dataset"
    analyze_folder(folder_path)