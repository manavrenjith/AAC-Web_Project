import json
import uuid
import shutil
import os
from typing import Dict, Any, cast

data_path = "c:/Users/ACER/OneDrive/Desktop/AAC-Web_Project/data.json"
upload_folder = "c:/Users/ACER/OneDrive/Desktop/AAC-Web_Project/static/images/custom"

# Ensure custom upload folder exists just in case
os.makedirs(upload_folder, exist_ok=True)

images = [
    {"src": "C:\\Users\\ACER\\.gemini\\antigravity\\brain\\1c257709-8bb3-4ccf-bf47-aa5930882a7a\\car_icon_1773511256871.png", "word": "Car", "category": "Vehicles"},
    {"src": "C:\\Users\\ACER\\.gemini\\antigravity\\brain\\1c257709-8bb3-4ccf-bf47-aa5930882a7a\\red_icon_1773511274230.png", "word": "Red", "category": "Colors"},
    {"src": "C:\\Users\\ACER\\.gemini\\antigravity\\brain\\1c257709-8bb3-4ccf-bf47-aa5930882a7a\\rose_icon_1773511291985.png", "word": "Rose", "category": "Flowers"},
    {"src": "C:\\Users\\ACER\\.gemini\\antigravity\\brain\\1c257709-8bb3-4ccf-bf47-aa5930882a7a\\eye_icon_1773511311324.png", "word": "Eye", "category": "Human Body Parts"},
    {"src": "C:\\Users\\ACER\\.gemini\\antigravity\\brain\\1c257709-8bb3-4ccf-bf47-aa5930882a7a\\dog_icon_1773511372618.png", "word": "Dog", "category": "Animals"},
    {"src": "C:\\Users\\ACER\\.gemini\\antigravity\\brain\\1c257709-8bb3-4ccf-bf47-aa5930882a7a\\apple_icon_1773511393650.png", "word": "Apple", "category": "Fruits"},
]

data: Dict[str, Any] = {}
try:
    with open(data_path, "r", encoding="utf-8") as f:
        data = cast(Dict[str, Any], json.load(f))
except FileNotFoundError:
    print("data.json not found")
    data = {"users": {}, "icons": [], "categories": []}

for img in images:
    new_id = str(uuid.uuid4())
    ext = ".png"
    new_filename = f"{new_id}_generated{ext}"
    dest = os.path.join(upload_folder, new_filename)
    
    if os.path.exists(img["src"]):
        shutil.copy(img["src"], dest)
        icons_list = data.get("icons", [])
        if not isinstance(icons_list, list):
            icons_list = []
        icons_list = cast(list, icons_list)
            
        icons_list.append({
            "id": new_id,
            "word": img["word"],
            "type": img["category"],
            "is_emoji": False,
            "content": f"custom/{new_filename}"
        })
        data["icons"] = icons_list
        print(f"Added {img['word']}")
    else:
        print(f"Image source missing for {img['word']}: {img['src']}")

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Update complete.")
