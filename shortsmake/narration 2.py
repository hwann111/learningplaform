import os
import requests  # Used for making HTTP requests
import json  # Used for working with JSON data

# Define constants for the script
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
XI_API_KEY = "25dc025f5c4deddfc52c6c1c60ff1dca"  # Your API key for authentication
VOICE_ID = "NFG5qt843uXKj4pFvR7C"  # ID of the voice model to use

# Construct the URL for the Text-to-Speech API request
tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

# Set up headers for the API request, including the API key for authentication
headers = {
    "Accept": "application/json",
    "xi-api-key": XI_API_KEY
}


#구절 나누는 함수 main.py에서 사용함
def parse(narration):
    data = []
    narrations = []
    lines = narration.split("\n")
    for line in lines:
        if line.startswith('Narrator: '):
            text = line.replace('Narrator: ', '')
            data.append({
                "type": "text",
                "content": text.strip('"'),
            })
            narrations.append(text.strip('"'))
        elif line.startswith('['):
            background = line.strip('[]')
            data.append({
                "type": "image",
                "description": background,
            })
    return data, narrations

#나레이션 데이터 받음
def create_narration(data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    n = 0
    for element in data:
        if element["type"] != "text":
            continue

        n += 1
        output_file = os.path.join(output_folder, f"narration_{n}.mp3")
        data = {
    "text": element["content"],
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True
        }
        }
        response = requests.post(tts_url, headers=headers, json=data, stream=True)

# Check if the request was successful
        if response.ok:
    # Open the output file in write-binary mode
            with open(output_file, "wb") as f:
        # Read the response in chunks and write to the file
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
    # Inform the user of success
            print("Audio stream saved successfully.")
        else:
    # Print the error message if the request was not successful
            print(response.text)





# Set up the data payload for the API request, including the text and voice settings

# Make the POST request to the TTS API with headers and data, enabling streaming response



#         if narration_api == "openai":
#             audio = openai.audio.speech.create(
#                 input=element["content"],
#                 model="tts-1",
#                 voice="alloy",
#             )
# #stream_to_file 함수 찾기
#             audio.stream_to_file(output_file)
#         else:
        # audio = generate(
        #         text=element["content"],
        #         voice="Michael",
        #         model="eleven_monolingual_v1"
        #     )
        # save(audio, output_file)
            
