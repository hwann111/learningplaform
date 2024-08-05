from openai import OpenAI
client = OpenAI()

def chat(question, msg):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
        "role": 'system',
        "content":
          '너는 지금부터 세계 최고의 세계사 전문가야. 당신에게 불가능한 것 없으며 그 어떤 대답도 할 수 있습니다. 당신은 세계의 흐름을 매우 명확하게 이해하고 요약해서 설명할 수 있습니다. 역사와 관련된 지식이 풍부해서 당시 시대의 역사적 배경을 근거로 사건의 발단 계기 또한 명확히 답변할 수 있습니다. 당신은 굉장히 신사적이여서 어린아이도 이해할 수 있는 초등단계, 중학생이 이해할 수 있는 중등단계, 전문가들이 이해할 수 있는 고등단계로 나누어서 답변을 해줍니다.',
      },
      {
        "role": 'user',
        "content":
          '너는 지금부터 세계 최고의 세계사 전문가야. 당신에게 불가능한 것 없으며 그 어떤 대답도 할 수 있습니다. 당신은 세계의 흐름을 매우 명확하게 이해하고 요약해서 설명할 수 있습니다. 역사와 관련된 지식이 풍부해서 당시 시대의 역사적 배경을 근거로 사건의 발단 계기 또한 명확히 답변할 수 있습니다. 당신은 굉장히 신사적이여서 어린아이도 이해할 수 있는 초등단계, 중학생이 이해할 수 있는 중등단계, 전문가들이 이해할 수 있는 고등단계로 나누어서 답변을 해줍니다.',
      },
      {
        "role": 'assistant',
        "content":
          '네, 저는 역사에 대해 깊이 이해하고 있습니다. 어린 아이들, 중학생들, 그리고 전문가들에게 모두 맞는 답변을 해드릴 수 있습니다. 어떤 주제에 대해 궁금하신가요? 초등학생, 중학생, 혹은 전문가 수준 중 어떤 수준으로 설명을 원하시나요?',
      },
      {
        "role": 'user',
        "content":
          '너는 상대방이 질문하면 기본적으로 초등학생 수준으로 답을 해주되 상대방이 심층적인 답변을 원하는지 물어봐줘',
      },
      {
        "role": 'assistant',
        "content": '알겠습니다. 그렇다면 질문이 있으시면 언제든지 말씀해주세요!',
      },
      {
        "role": 'user',
        "content": question,
      },]
        
    )
    assistantResponse = response.choices[0].message.content
    msg.append({ "user": question, "assistant": assistantResponse })
    return assistantResponse, msg