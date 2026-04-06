import os
from app.services.yolo_service import detect_and_crop
from app.services.gemini_service import analyze_image
from app.services.video_service import extract_frames


def process_image(image_path):
    """
    Process a single image (or frame) without relying on YOLO.
    Returns one consolidated AI result per animal.
    """
    # Instead of detect_and_crop, we just analyze the full frame
    ai_results = analyze_image(image_path)  # returns list of dicts

    # Dictionary to merge multiple detections of the same animal
    animals_dict = {}
    
    for animal in ai_results:
        # Use species + gender + age as a key to identify unique animals
        animal_key = (
            animal.get("Animal_Species", "").lower(),
            animal.get("Gender", "").lower(),
            animal.get("Age", "").lower()
        )
        
        if animal_key not in animals_dict:
            # First occurrence
            animals_dict[animal_key] = {
                "frame": os.path.basename(image_path),
                **animal
            }
        else:
            # Merge observations from multiple detections (if any)
            existing_obs = animals_dict[animal_key].get("Observations", "")
            new_obs = animal.get("Observations", "")
            if new_obs and new_obs not in existing_obs:
                animals_dict[animal_key]["Observations"] = existing_obs + " " + new_obs

    # Assign sequential Unique_IDs
    results = []
    for idx, animal_info in enumerate(animals_dict.values(), start=1):
        animal_info["Unique_ID"] = f"wl_{idx:03d}"
        results.append(animal_info)

    return results


def process_video(video_path):
    frames = extract_frames(video_path)

    all_results = []

    for frame in frames:
        frame_results = process_image(frame)
        all_results.extend(frame_results)

    return all_results


def analyze_media(file_path, file_type):
    if file_type == "image":
        return process_image(file_path)

    elif file_type == "video":
        return process_video(file_path)

    return {"error": "Unsupported file"}