import os
import json
from narration import parse
from video import create
def test(): 
    font_path = "font/BMEULJIROTTF.ttf"

    basedir = os.path.join("shorts", "1718251498")
    output_file = "short.avi"
    with open(os.path.join(basedir, "response.txt"), "r") as f:
        response_text = f.read()

    data, narrations = parse(response_text)
    with open(os.path.join(basedir, "data.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)

    print("Generating video...")
    create(narrations, basedir, output_file, font_path)

    print(f"DONE! Here's your video: {os.path.join(basedir, output_file)}")
    path = str(os.path.join(basedir, output_file))
    return  path

# print(test())
