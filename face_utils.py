
from deepface import DeepFace
from pathlib import Path

def find_face(img_path, db_path="dataset"):
    try:
        results = DeepFace.find(img_path=img_path, db_path=db_path, enforce_detection=False)

        if isinstance(results, list) and len(results) > 0:
            match = results[0]
            if hasattr(match, 'empty'):
                if not match.empty and 'identity' in match.columns:
                    return Path(match.iloc[0]['identity']).stem
            elif isinstance(match, dict):
                return Path(match.get("identity", "Unknown")).stem
        return "Unknown"

    except Exception as e:
        print("Error in find_face:", e)
        return "Error"

