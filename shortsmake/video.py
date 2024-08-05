from pydub import AudioSegment
import numpy as np
import math
import cv2
import os

from text import add_narration_to_video

font_path = "font/BMEULJIROTTF.ttf"
#오디오 파일 입히기
def get_audio_duration(audio_file):
    return len(AudioSegment.from_file(audio_file))
#이미지 크기 정하기
def resize_image(image, width, height):
    # Calculate the aspect ratio of the original image
    aspect_ratio = image.shape[1] / image.shape[0]

    # Calculate the new dimensions to fit within the desired size while preserving aspect ratio
    if aspect_ratio > (width / height):
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        new_height = height
        new_width = int(height * aspect_ratio)

    # Resize the image to the new dimensions without distorting it
    return cv2.resize(image, (new_width, new_height))


def create(narrations, output_dir, output_filename, font_path):
    # Define the dimensions and frame rate of the video
    width, height = 1080, 1920  # Change as needed for your vertical video
    frame_rate = 30  # Adjust as needed 30 프레임이라는 뜻

    fade_time = 1000

    # Create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
    temp_video = os.path.join(output_dir, "temp_video.avi")  # Output video file name
    #비디오 저장하기 VideoWriter(영상주소, 형식?, 프레임, 사이즈)
    out = cv2.VideoWriter(temp_video, fourcc, frame_rate, (width, height))


    # List of image file paths to use in the video
    image_paths = os.listdir(os.path.join(output_dir, "images"))  # Replace with your image paths
    image_count = len(image_paths)

    # Load images and perform the transition effect
    #이미지 한장 당
    for i in range(image_count):
        image1 = cv2.imread(os.path.join(output_dir, "images", f"image_{i+1}.webp"))

        if i+1 < image_count:
            image2 = cv2.imread(os.path.join(output_dir, "images", f"image_{i+2}.webp"))
        else:
            image2 = cv2.imread(os.path.join(output_dir, "images", f"image_1.webp"))

        image1 = resize_image(image1, width, height)
        image2 = resize_image(image2, width, height)
        #narration에 나레이션 음성 파일 하나씩 넣음
        narration = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")
        duration = get_audio_duration(narration)

        if i > 0:
            duration -= fade_time

        if i == image_count-1:
            duration -= fade_time
            
#duration : 총 음성 길이
#floor() 반올림
        for _ in range(math.floor(duration/1000*30)):
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = image1
#write() 파일쓰기
            out.write(vertical_video_frame)
#linspace : 수평축 간격 만들기 함수 
#이미지 변환 속도, 이미지별 시간 간격
        for alpha in np.linspace(0, 1, math.floor(fade_time/1000*30)):
            blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = blended_image

            out.write(vertical_video_frame)

    # Release the VideoWriter and close the window if any
    out.release()
    cv2.destroyAllWindows()

    add_narration_to_video(narrations, temp_video, output_dir, output_filename, font_path)

    os.remove(temp_video)
