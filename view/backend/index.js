import OpenAI from 'openai';
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { log } from 'console';
import bodyParser from 'body-parser';

dotenv.config(); // 환경 변수 설정

// ES 모듈 스코프에서 __dirname을 해결하는 방법
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize Express
const app = express();
const PORT = 3000;

// CORS 설정
app.use(cors());

// POST 요청 받을 수 있도록 설정
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 정적 파일 제공
app.use(express.static(path.join(__dirname, '../public')));

// 대화 기록 배열
let messages = [];

// OPENAI 설정
const openai = new OpenAI({
  apiKey: 'secret',
});

// POST method
app.post('/eduCation', async function (req, res) {
  const question = req.body.question;
  const chatCompletion = await openai.chat.completions.create({
    max_tokens: 2000,
    messages: [
      {
        role: 'system',
        content:
          '너는 지금부터 세계 최고의 세계사 전문가야. 당신에게 불가능한 것 없으며 그 어떤 대답도 할 수 있습니다. 당신은 세계의 흐름을 매우 명확하게 이해하고 요약해서 설명할 수 있습니다. 역사와 관련된 지식이 풍부해서 당시 시대의 역사적 배경을 근거로 사건의 발단 계기 또한 명확히 답변할 수 있습니다. 당신은 굉장히 신사적이여서 어린아이도 이해할 수 있는 초등단계, 중학생이 이해할 수 있는 중등단계, 전문가들이 이해할 수 있는 고등단계로 나누어서 답변을 해줍니다.',
      },
      {
        role: 'user',
        content:
          '너는 지금부터 세계 최고의 세계사 전문가야. 당신에게 불가능한 것 없으며 그 어떤 대답도 할 수 있습니다. 당신은 세계의 흐름을 매우 명확하게 이해하고 요약해서 설명할 수 있습니다. 역사와 관련된 지식이 풍부해서 당시 시대의 역사적 배경을 근거로 사건의 발단 계기 또한 명확히 답변할 수 있습니다. 당신은 굉장히 신사적이여서 어린아이도 이해할 수 있는 초등단계, 중학생이 이해할 수 있는 중등단계, 전문가들이 이해할 수 있는 고등단계로 나누어서 답변을 해줍니다.',
      },
      {
        role: 'assistant',
        content:
          '네, 저는 역사에 대해 깊이 이해하고 있습니다. 어린 아이들, 중학생들, 그리고 전문가들에게 모두 맞는 답변을 해드릴 수 있습니다. 어떤 주제에 대해 궁금하신가요? 초등학생, 중학생, 혹은 전문가 수준 중 어떤 수준으로 설명을 원하시나요?',
      },
      {
        role: 'user',
        content:
          '너는 상대방이 질문하면 기본적으로 초등학생 수준으로 답을 해주되 상대방이 심층적인 답변을 원하는지 물어봐줘',
      },
      {
        role: 'assistant',
        content: '알겠습니다. 그렇다면 질문이 있으시면 언제든지 말씀해주세요!',
      },
      {
        role: 'user',
        content: question,
      },
    ],
    model: 'gpt-3.5-turbo',
  });

  const assistantResponse = chatCompletion.choices[0].message['content'];

  // 대화 기록에 추가
  messages.push({ user: question, assistant: assistantResponse });
  console.log(assistantResponse);
  // 클라이언트에게 Assistant의 답변 전송
  res.json({ assistant: assistantResponse, messages });
});

app.post('/fliplearning', async function (req, res) {
  const question = req.body.question;
  // const role = req.body.role;
  const role = "40대 아주머니"
  const chatCompletion = await openai.chat.completions.create({
    max_tokens: 150,
    messages: [
      {
        role: 'system',
        content:
          `너는 지금부터 역사에 대한 강의를 들을거야, 너는 ${role} 야, 너는 ${role}에 맞게 설명을 듣고 이해를 하고 대처를 해야해, 또 너는 ${question}에 대해 아무 지식이 없는 상태에서 너가 ${role} 이라는 것을 인지하고 설명을 듣고 어떤 것이 이해가 안되었는지 잘 말해 줄 수 있어야 해 `
      },
      {
        role: 'user',
        content:
          `너는 지금부터 역사에 대한 강의를 들을거야, 너는 ${role} 야, 너는 ${role}에 맞게 설명을 듣고 이해를 하고 대처를 해야해, 또 너는 ${question}에 대해 아무 지식이 없는 상태에서 너가 ${role} 이라는 것을 인지하고 설명을 듣고 어떤 것이 이해가 안되었는지 잘 말해 줄 수 있어야 해, 자 이제부터 상대에게 ${question}에 대해 설명해 달라고 ${role}에 맞게 말해봐`
      },
      {
        role: 'user',
        content: question,
      },
    ],
    model: 'gpt-3.5-turbo',
  });

  const assistantResponse = chatCompletion.choices[0].message['content'];

  // 대화 기록에 추가
  messages.push({ user: question, assistant: assistantResponse });
  console.log(assistantResponse);
  // 클라이언트에게 Assistant의 답변 전송
  res.json({ assistant: assistantResponse, messages });
});


// 전체 대화 기록 확인을 위한 엔드포인트
app.get('/chatHistory', function (req, res) {
  res.json({ messages });
});

// 서버 실행
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
