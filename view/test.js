function calculateResults() {
    const form = document.getElementById('vark-form');
    const results = { V: 0, A: 0, R: 0, K: 0 };
    const questions = 16; // 총 질문 수
  
    // 각 질문에 대해 선택된 답변을 계산
    for (let i = 1; i <= questions; i++) {
      const answer = form[`q${i}`].value;
      if (!answer) {
        alert(
          `문항 ${i}에 대한 답변이 선택되지 않았습니다. 모든 문항에 답변해주세요.`
        );
        return; // 함수 종료
      }
      results[answer]++;
    }
  
    // 결과를 배열로 변환하여 점수로 정렬
    const sortedResults = Object.entries(results).sort((a, b) => b[1] - a[1]);
  
    // 로컬 스토리지에 sortedResults 저장
    localStorage.setItem('sortedResults', JSON.stringify(sortedResults));
  
    // 가장 높은 점수의 두 항목 선택
    const topTwoResults = sortedResults.slice(0, 2);
  
    // 각 항목의 의미를 담은 객체
    const resultLabels = {
      V: 'V : 시각 선호 유형',
      A: 'A : 청각 선호 유형',
      R: 'R : 읽기, 쓰기 선호 유형',
      K: 'K : 경험 선호 유형',
    };
  
    // 결과를 페이지에 표시
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = topTwoResults
      .map(
        (result) => `
              <div class="results-card">
                  ${resultLabels[result[0]]}
              </div>
          `
      )
      .join('');
  
    // 다음 페이지로 이동하는 버튼을 보이게 하고 기존 버튼 숨기기
    const nextPageButton = document.getElementById('next-page-button');
    nextPageButton.style.display = 'inline-block';
    form.style.display = 'none'; // 기존의 form 숨기기
  }
  
  function goToNextPage() {
    window.location.href = 'start.html'; // 키워드 입력 페이지로 변경
  }
  