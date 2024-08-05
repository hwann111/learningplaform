async function sendMessage() {
  const userInput = document.getElementById('userInput');
  const messageContainer = document.getElementById('messages');

  const userMessage = userInput.value;

  // 사용자 메시지를 화면에 추가
  const userMessageElement = document.createElement('div');
  userMessageElement.classList.add('message', 'user-message');
  userMessageElement.textContent = userMessage;
  messageContainer.appendChild(userMessageElement);

  // 입력 필드 초기화
  userInput.value = '';

  try {
    const response = await fetch('http://localhost:3000/eduCation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: userMessage }),
    });

    const data = await response.json();
    const assistantMessage = data.assistant;

    // 어시스턴트 메시지를 화면에 추가
    const assistantMessageElement = document.createElement('div');
    assistantMessageElement.classList.add('message', 'bot-message');
    assistantMessageElement.textContent = assistantMessage;
    messageContainer.appendChild(assistantMessageElement);

    // 메시지 창 스크롤을 가장 아래로
    messageContainer.scrollTop = messageContainer.scrollHeight;
  } catch (error) {
    console.error('Error:', error);
  }
}
