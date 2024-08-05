#!/usr/bin/env python3
# 토큰 정보로드를 위한 라이브러리
# 설치: pip install python-dotenv
# from dotenv import load_dotenv

# # # 토큰 정보로드
# load_dotenv()
from openai import OpenAI
import time
import json
import sys
import os
from narration import parse, create_narration
from images import create_from_data
from video import create

client = OpenAI()

def shortmake(keyword):
    short_id = str(int(time.time()))
    output_file = "short.avi"
    font_path = "font/BMEULJIROTTF.ttf"

#shorts폴더 아래 short_id(시간)로 폴더 생성
    basedir = os.path.join("shorts", short_id)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    print("Generating script...")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
        {
            "role": "system",
            #여기에 있는 것을 조금 수정
            "content": """You are a YouTube short narration generator. You generate 30 seconds to 1 minute of narration. The shorts you create have a background that fades from image to image as the narration is going on.

You will need to generate descriptions of images for each of the sentences in the short. They will be passed to an AI image generator. DO NOT IN ANY CIRCUMSTANCES use names of celebrities or people in the image descriptions. It is illegal to generate images of celebrities. Only describe persons without their names. Do not reference any real person or group in the image descriptions. Don't mention the female figure or other sexual content in the images because they are not allowed.

You are however allowed to use any content, including real names in the narration. Only image descriptions are restricted.

Note that the narration will be fed into a text-to-speech engine, so don't use special characters.

Respond with a pair of an image description in square brackets and a narration below it. Both of them should be on their own lines, as follows:

###

[Description of a background image]

Narrator: "One sentence of narration"

[Description of a background image]

Narrator: "One sentence of narration"

[Description of a background image]

Narrator: "One sentence of narration"

###

The short should be 6 sentences maximum.

You should add a description of a fitting backround image in between all of the narrations. It will later be used to generate an image with AI.
"""
        },
        {
            "role": "user",
            "content": f"Create a YouTube short in Korean narration based on the following source material:\n\n{keyword}"
        }
    ]
    )

    print("response: ", response)


    response_text = response.choices[0].message.content
    print("response_txt:  ",response_text)
    response_text.replace("’", "'").replace("`", "'").replace("…", "...").replace("“", '"').replace("”", '"')

    print("2:/", response_text)

    with open(os.path.join(basedir, "response.txt"), "w") as f:
        f.write(response_text)

    data, narrations = parse(response_text)
    with open(os.path.join(basedir, "data.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"Generating narration...")
    create_narration(data, os.path.join(basedir, "narrations"))

    print("Generating images...")
    create_from_data(data, os.path.join(basedir, "images"))

    print("Generating video...")
    create(narrations, basedir, output_file, font_path)

    print(f"DONE! Here's your video: {os.path.join(basedir, output_file)}")
    video_path = {os.path.join(basedir, output_file)}
    return video_path

# shortmake("병자호란")
