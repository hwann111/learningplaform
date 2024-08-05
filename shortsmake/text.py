from pydub import AudioSegment
import numpy as np
import math
import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import subprocess


font_path = "font/BMEULJIROTTF.ttf"

def get_audio_duration(audio_file):
    return len(AudioSegment.from_file(audio_file))

def write_text(text, frame, video_writer, font_path):
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    text_size = draw.textbbox((0, 0), text, font=font)
    # text_x = (frame.shape[1] - text_size[0]) // 2
    # text_y = (frame.shape[0] - text_size[1]) // 2
    text_x = frame.shape[1] // 2
    text_y = frame.shape[0] // 2
    text_width = text_size[2] - text_size[0]
    text_height = text_size[3] - text_size[1]
    text_size = (text_width, text_height)

    outline_color = 'black'
    text_x = text_x - (text_size[0]//2)
    text_y = text_y - (text_size[1] // 2)
    
    draw.text((text_x-2, text_y-2), text, font=font, fill=outline_color)
    draw.text((text_x+2, text_y-2), text, font=font, fill=outline_color)
    draw.text((text_x-2, text_y+2), text, font=font, fill=outline_color)
    draw.text((text_x+2, text_y+2), text, font=font, fill=outline_color)
    
    draw.text((text_x, text_y ), text, font=font, fill="white")
    
    frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    video_writer.write(frame)
    
def split_text_into_chunks(text, max_length=100):
    words = text.split(" ")
    chunks = []
    current_chunk = []

    for word in words:
        # Adding the word to the current chunk and a space
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            # If adding the word exceeds the max_length, finalize the current chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def add_narration_to_video(narrations, input_video, output_dir, output_file, font_path):
    cap = cv2.VideoCapture(input_video)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    temp_video = os.path.join(output_dir, "with_transcript.avi")
    out = cv2.VideoWriter(temp_video, fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

    full_narration = AudioSegment.empty()
    offset = 200
    x = 2
    for i, narration in enumerate(narrations):
        audio = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")
        duration = get_audio_duration(audio)
        narration_frames = math.floor(duration / 1000 * 30)

        full_narration += AudioSegment.from_file(audio)
        
        char_count = len(narration.replace(" ", ""))
        ms_per_char = duration / char_count

        frames_written = 0
        #여기 띄어쓰기 ㄱㅣ준 수정
        # words = narration.split(" ")
        words = split_text_into_chunks(narration, max_length=10)
        for w, word in enumerate(words):
            
            #여기 출력 시간 수정
            word_ms = len(word) * ms_per_char

            if i == 0 and w == 0:
                # x *= x
                # offset += offset*x
                word_ms -= offset
                if word_ms < 0:
                    word_ms = 0

            for _ in range(math.floor(word_ms / 1000 * 25)):
                ret, frame = cap.read()
                if not ret:
                    break
                write_text(word, frame, out, font_path)
                frames_written += 1

        for _ in range(narration_frames - frames_written):
            ret, frame = cap.read()
            out.write(frame)

    while out.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    temp_narration = os.path.join(output_dir, "narration.mp3")
    full_narration.export(temp_narration, format="mp3")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-i', temp_video,
        '-i', temp_narration,
        '-map', '0:v',
        '-map', '1:a',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        os.path.join(output_dir, output_file)
    ]

    subprocess.run(ffmpeg_command, capture_output=True)

    os.remove(temp_video)
    os.remove(temp_narration)

