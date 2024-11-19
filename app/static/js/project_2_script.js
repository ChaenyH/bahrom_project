function convertCurrency() {
    const destination = document.getElementById('destination').value;
    const budget = document.getElementById('budget').value;
    let rate = 1;

    if (destination.includes('미국')) rate = 1200;
    else if (destination.includes('일본')) rate = 10;

    const converted = budget * rate;
    document.getElementById('converted-currency').innerText = `${converted} 원`;
}

function addExpense() {
    const expense = parseInt(document.getElementById('expense').value);
    const description = document.getElementById('description').value;

    if (!expense) return alert('소비 금액을 입력하세요.');

    const expenseList = document.getElementById('expense-list');
    const listItem = document.createElement('li');
    listItem.innerText = `${description} - ${expense} 원`;
    expenseList.appendChild(listItem);
}
