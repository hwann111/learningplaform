// data변수에 키워드로 입력한 데이터 나오게 하기
// 받은 데이터 parent, children 으로 바꾸기

// Fetch API를 사용하여 FastAPI 서버에서 변수 가져오기
async function fetchVariable() {
    try {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const keyword = urlParams.get('keyword')
        const url = `http://localhost:8000/get-variable?keyword=${encodeURIComponent(keyword)}`;
        const response = await fetch(url);
        
        const data = await response.json();
       
        console.log(data);
        generateMindmap(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

// 데이터를 처리하는 함수
function processData(variable) {
    // 예시: 받은 문자열을 대문자로 변환하고 강조 스타일 적용
    const processed = variable.toUpperCase();
    const processedOutputElement = document.getElementById('processed-output');
    processedOutputElement.innerText = processed;
    processedOutputElement.classList.add('highlight');
}


function generateMindmap(data) {
    const keywordElement = document.getElementById('keyword');
    const nodesContainer = document.getElementById('nodes');

    keywordElement.textContent = data.keyword;

    data.nodes.forEach(node => {
        const nodeElement = document.createElement('div');
        nodeElement.className = 'node';

        const parentElement = document.createElement('div');
        parentElement.className = 'parent-node';
        parentElement.textContent = node.parent;
        nodeElement.appendChild(parentElement);
        // 자식노드버튼
        node.children.forEach(child => {
            const childButton = document.createElement('button');
            childButton.className = 'child-node';
            childButton.textContent = child.question;
            childButton.addEventListener('click', () => {
                // alert(child);
                //여기 수정 추가
                openPopup(child.question, child.answer);
            });
            nodeElement.appendChild(childButton);
        });

        nodesContainer.appendChild(nodeElement);
    });
}

function openPopup(childData, answer) {
    const popup = document.createElement('div');
    popup.className = 'popup';

    const childDiv = document.createElement('div');
    childDiv.textContent = childData;

    const inputDiv = document.createElement('div');
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputDiv.appendChild(inputField);

    const answerDiv = document.createElement('div');
    answerDiv.id = 'answer-div';

    const answerButton = document.createElement('button');
    answerButton.textContent = '정답';
    //여기에 정답 데이터
    answerButton.className = 'answer-button';
    answerButton.addEventListener('click', () => {
        answerDiv.textContent = answer; // 정답을 표시
    });

    popup.appendChild(childDiv);
    popup.appendChild(inputDiv);
    popup.appendChild(answerButton);
    popup.appendChild(answerDiv);

    const closeButton = document.createElement('button');
    closeButton.textContent = '닫기';
    closeButton.addEventListener('click', () => {
        document.body.removeChild(popup);
    });

    popup.appendChild(closeButton);

    document.body.appendChild(popup);

    // 팝업 스타일 설정
    popup.style.position = 'fixed';
    popup.style.top = '50%';
    popup.style.left = '50%';
    popup.style.transform = 'translate(-50%, -50%)';
    popup.style.backgroundColor = 'white';
    popup.style.border = '1px solid black';
    popup.style.padding = '20px';
    popup.style.zIndex = 1000;
    popup.style.width = '80%';
    popup.style.height = '60%';
    popup.style.display = 'flex';
    popup.style.flexDirection = 'column';
    popup.style.alignItems = 'center';
    popup.style.justifyContent = 'space-around';

    childDiv.style.marginBottom = '10px';
    inputDiv.style.marginBottom = '10px';
    inputDiv.style.backgroundColor = ""
    inputDiv.style.width = "50%";
    inputDiv.style.height = "20%";

    inputField.style.marginTop = '20px';
    inputField.style.width = '100%';
    inputField.style.height = '100%';
    
    answerDiv.style.marginTop = '20px';

    // 정답 버튼 스타일 설정
    answerButton.style.padding = '10px 20px';
    answerButton.style.borderRadius = '10px';
    answerButton.style.backgroundColor = 'blue';
    answerButton.style.color = 'white';
    answerButton.style.fontSize = '18px';
    answerButton.style.border = '3px solid blue';
    answerButton.style.marginTop = '20px';
    answerButton.style.cursor = 'pointer';
}

document.addEventListener('DOMContentLoaded', () => {
    fetchVariable();
    // generateMindmap(data);
});
