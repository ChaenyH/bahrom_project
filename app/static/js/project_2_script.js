document.getElementById("budget-form").addEventListener("submit", function (e) {
    e.preventDefault(); // 폼 제출 방지
    convertCurrency();
});

document.getElementById("expense-form").addEventListener("submit", function (e) {
    e.preventDefault(); // 폼 제출 방지
    addExpense();
});


// 환율 데이터 동적 처리

async function fetchExchangeRate(destination) {
    const response = await fetch(`https://api.exchangerate-api.com/v4/latest/USD`);
    const data = await response.json();
    const rate = destination.includes('미국') ? data.rates.KRW : 
                 destination.includes('일본') ? data.rates.JPY : 1;
    return rate;
}

async function convertCurrency() {
    const destination = document.getElementById('destination').value;
    const budget = document.getElementById('budget').value;
    const rate = await fetchExchangeRate(destination);
    const converted = budget * rate;
    document.getElementById('converted-currency').innerText = `${converted} 원`;
}

// 잔여 예산 업데이트

let totalBudget = 0;

function setBudget() {
    totalBudget = parseInt(document.getElementById('budget').value);
    document.getElementById('remaining-budget').innerHTML = `남은 예산: <strong>${totalBudget} 원</strong>`;
}

function addExpense() {
    const expense = parseInt(document.getElementById('expense').value);
    const description = document.getElementById('description').value;

    if (!expense) return alert('소비 금액을 입력하세요.');

    const expenseList = document.getElementById('expense-list');
    const listItem = document.createElement('li');
    listItem.innerText = `${description} - ${expense} 원`;
    expenseList.appendChild(listItem);

    totalBudget -= expense;
    document.getElementById('remaining-budget').innerHTML = `남은 예산: <strong>${totalBudget} 원</strong>`;
}

function evaluateTrip() {
    console.log("여행 평가 로직 실행");
    document.getElementById('evaluation-result').innerText = "평가 결과: 윤리적 소비가 잘 실천되었습니다!";
}

function chatWithBot() {
    console.log("Chatbot interaction initiated");
    const input = document.getElementById('chat-input').value;
    const responseDiv = document.getElementById('chat-response');

    // Example response logic
    if (input.toLowerCase().includes('윤리적 소비')) {
        responseDiv.innerText = "윤리적 소비는 환경과 사회를 고려한 소비입니다!";
    } else {
        responseDiv.innerText = "챗봇과의 대화가 등록되지 않았습니다. 더 구체적인 질문을 입력해 주세요.";
    }
}
