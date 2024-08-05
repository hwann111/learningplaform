from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mindmap import generate_question
import json
import time
import threading

from openai import OpenAI 
import logging
from urllib.parse import urlparse, parse_qs
import cgi
from shortmake import shortmake
from test import test
 
# from shortsmake.narration import parse, create

app = FastAPI()



# 예제 변수
@app.get("/get-variable")
async def get_variable(keyword: str = Query(...)):
    # nodes = json.loads(content)
    print("호출됨1")
    print("2")
    # content.replace("\","")
    
    keyword, nodes = generate_question(keyword)
    return JSONResponse(content={"keyword": keyword, "nodes": nodes})

# @app.get("/get-video")
# async def get_video(keyword: str = Query(...)):
   
    
#     path = shortmake(keyword)
#     return path


# def generate_video():
#     global video_generated
#     path = test()  # 비디오 생성 시뮬레이션 (예: 10초 후 생성 완료)
#     video_generated = True


# @app.get("/start_video_generation")
# async def start_video_generation():
#     global video_generated
#     video_generated = False  # 비디오 생성 상태 초기화
#     threading.Thread(target=generate_video).start()  # 비디오 생성 작업 시작
#     return JSONResponse(content={"message": "Video generation started"})

# @app.get("/check_video_status")
# async def check_video_status():
#     return JSONResponse(content={"generated": video_generated, "path": "/shorts/generated_video/short.avi"})

# @app.get("/start_video_generation")
# async def get_video(keyword: str = Query(...)):
#     print("생성중")
#     path = test()
    
#     return JSONResponse(content={"path": path})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (보안상 필요한 출처만 허용하도록 설정 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# def validate_messages(messages):
#     for message in messages:
#         if not isinstance(message, dict):
#             raise ValueError("Each message must be a dictionary")
#         if "role" not in message or "content" not in message:
#             raise ValueError("Each message must have 'role' and 'content' keys")
#         if not isinstance(message["content"], str):
#             raise ValueError("'content' must be a string")
# @app.post("/eduCation")
# async def post_education(question: Question):
#     user_question = question.question
    
#     validate_messages(messages)
#     messages = []
#     assistantResponse, messages = chat(question, messages)
#     try:
#         body = await request.json()
#         question = body.get("question")
#         messages = body.get("messages")
        
#         # Validate the messages structure
#         validate_messages(messages)

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages
#         )

#         assistant_response = response['choices'][0]['message']['content']
#         return JSONResponse(content={"response": assistant_response})
    
#     except openai.error.OpenAIError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     return JSONResponse(content={ "assistant": assistantResponse,  }),messages



# app.get('/chatHistory', function (req, res) {
#   res.json({ messages });
# });

# @app.get("/chatHistory")
# def get_chatHistory():
    
#     return JSONResponse("messages":messages)
# client = OpenAI()
# @app.post("/eduCation")
# async def post_education(request: Request):
#     # 요청 본문을 로그에 출력
#     logging.info("Received request: %s", await request.body())
    
#     try:
#         body = await request.json()
#     except Exception as e:
#         logging.error("Failed to parse request body: %s", str(e))
#         return JSONResponse(content={"error": "Invalid JSON"}, status_code=400)
#     question = body.get("question")
    
#     messages = [
#         {
#             "role": "system",
#             "content": "너는 지금부터 세계 최고의 세계사 전문가야. 당신에게 불가능한 것 없으며 그 어떤 대답도 할 수 있습니다. 당신은 세계의 흐름을 매우 명확하게 이해하고 요약해서 설명할 수 있습니다. 역사와 관련된 지식이 풍부해서 당시 시대의 역사적 배경을 근거로 사건의 발단 계기 또한 명확히 답변할 수 있습니다. 당신은 굉장히 신사적이여서 어린아이도 이해할 수 있는 초등단계, 중학생이 이해할 수 있는 중등단계, 전문가들이 이해할 수 있는 고등단계로 나누어서 답변을 해줍니다."
#         },
#         {
#             "role": "user",
#             "content": "너는 지금부터 세계 최고의 세계사 전문가야. 당신에게 불가능한 것 없으며 그 어떤 대답도 할 수 있습니다. 당신은 세계의 흐름을 매우 명확하게 이해하고 요약해서 설명할 수 있습니다. 역사와 관련된 지식이 풍부해서 당시 시대의 역사적 배경을 근거로 사건의 발단 계기 또한 명확히 답변할 수 있습니다. 당신은 굉장히 신사적이여서 어린아이도 이해할 수 있는 초등단계, 중학생이 이해할 수 있는 중등단계, 전문가들이 이해할 수 있는 고등단계로 나누어서 답변을 해줍니다."
#         },
#         {
#             "role": "assistant",
#             "content": "네, 저는 역사에 대해 깊이 이해하고 있습니다. 어린 아이들, 중학생들, 그리고 전문가들에게 모두 맞는 답변을 해드릴 수 있습니다. 어떤 주제에 대해 궁금하신가요? 초등학생, 중학생, 혹은 전문가 수준 중 어떤 수준으로 설명을 원하시나요?"
#         },
#         {
#             "role": "user",
#             "content": "너는 상대방이 질문하면 기본적으로 초등학생 수준으로 답을 해주되 상대방이 심층적인 답변을 원하는지 물어봐줘"
#         },
#         {
#             "role": "assistant",
#             "content": "알겠습니다. 그렇다면 질문이 있으시면 언제든지 말씀해주세요!"
#         },
#         {
#             "role": "user",
#             "content": question,
#         },
#     ]

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )

#     assistant_response = response['choices'][0]['message']['content']

#     return JSONResponse(content={"assistant": assistant_response})