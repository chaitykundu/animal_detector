import json
import pandas as pd
import os


def generate_excel_report(json_file_path):
    # Check file exists
    if not os.path.exists(json_file_path):
        print(f"JSON file not found: {json_file_path}")
        return

    # Load JSON data
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # If single object → convert to list
    if isinstance(data, dict):
        data = [data]

    rows = []

    for item in data:
        row = {
            "Animal_ID": item.get("Animal_ID", ""),
            "Species": item.get("Species", ""),
            "Gender": item.get("Gender", ""),
            "Age": item.get("Age", ""),
            "Pregnancy_Status": item.get("Pregnancy_Status", "")
        }

        # Health details
        health = item.get("Health_Status", {})
        row["Health_Condition"] = health.get("Condition", "")
        row["Likely_Disease"] = health.get("Likely_Disease", "")
        row["Management_Tips"] = health.get("Management_Tips", "")

        # Antlers/Horns details
        antlers = item.get("Antlers_Horns", {})
        row["Antlers_Type"] = antlers.get("Type", "")
        row["Antlers_Condition"] = antlers.get("Condition", "")
        row["Antlers_Notes"] = antlers.get("Notes", "")

        rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Output file path
    excel_path = json_file_path.replace(".json", ".xlsx")

    # Save Excel
    df.to_excel(excel_path, index=False)

    print(f"Excel report generated successfully!")
    print(f"Saved at: {excel_path}")


if __name__ == "__main__":
    json_path = r"C:\Users\Chaity Kundu\Desktop\Chaity\animal\dataset\analysis_results.json"
    generate_excel_report(json_path)