from openai import OpenAI
import json

client = OpenAI()
def generate_question(keyword):
    # keyword = "봉오동전투"
    # keyword = input("키워드 입력하세요: ")
    
    print(f"{keyword}에 대한 자료 생성중...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
          
             "content": """ 너는 아주 유능한 선생님이야, 너는 주어진 키워드에 맞춘 몇개의 토론 질문과 그 질문에 대한 답을 만들어 내야해
             예시로 임진왜란에 대한 키워드를 받았을 때의 출력 형식을 보여줄게




    [
    {
        "parent": "병자호란의 배경과 원인",
        "children": [
            {
                "question": "병자호란이 발발한 배경과 원인에는 어떤 역사적 사건과 정치적 요인이 작용했는가?",
                "answer": "경제적 위기와 정치적 불안, 만주족의 침입과 영토 요구"
            },
            {
                "question": "왜 조선은 만주가 침입했을 때 즉각적인 대응을 하지 못했는가?",
                "answer": "왕권의 약화와 군비 감축으로 전력이 부족, 시대 정세 변화에 대처 못 함"
            }
        ]
    },
    {
        "parent": "병자호란의 전투와 전략",
        "children": [
            {
                "question": "병자호란에서 주요 전투와 전략은 무엇이 있었으며, 어떻게 전략의 성패가 결정되었는가?",
                "answer": "희곡대전과 율도군사정벌, 전투 전략의 부재와 장수의 부재"
            },
            {
                "question": "왜 조선군은 병자호란에서 패배를 거두었는가?",
                "answer": "전략의 부재와 인원 부족, 잘못된 전투 결정과 부대 분배"
            }
        ]
    },
    {
        "parent": "병자호란의 영향과 결과",
        "children": [
            {
                "question": "병자호란이 조선에 어떤 영향을 끼쳤으며, 후세의 국가 발전에 어떤 변화를 가져왔는가?",
                "answer": "조선의 국력 약화와 한 치의 건 전 없음, 임진왜란으로 이어지는 국가 위기"
            },
            {
                "question": "병자호란으로부터 얻을 수 있는 역사적 교훈은 무엇이 될까?",
                "answer": "강한 외교력과 뛰어난 군사력의 중요성, 국가 안보를 위한 전략 수립의 필요성"
            }
        ]
    },
    {
        "parent": "병자호란과 동북아시아 정세",
        "children": [
            {
                "question": "병자호란이 동북아시아 정세에 미친 영향은 무엇이었고, 조선의 국제적 입장은 어땠는가?",
                "answer": "만주족과 일본의 동아시아 침공 압력, 중국과의 역사적 협력 및 연약함"
            },
            {
                "question": "병자호란으로 인해 조선은 어떤 국제적 위치와 역할을 갖게 되었는가?",
                "answer": "외교적 약화와 군사적 소외, 동북아시아에서의 영토 견인 권리 상실"
            }
        ]
    }
        ]



 이런 식으로 키워드를 받았을 때 토론 질문과 답을 만들면 됨

"""
        },
        {
            "role": "user",
            "content": f"{keyword}에 대한 토론 질문과 답을 생성해줘"
        }
    ]
)
    print(response)
    nodes = response.choices[0].message.content
    print(nodes)
    # JSON 데이터 파싱
    nodes = json.loads(nodes)

    
    return keyword, nodes
