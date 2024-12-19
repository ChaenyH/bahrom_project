document.addEventListener('DOMContentLoaded', () => {
    const chatSendButton = document.getElementById('chat-send-button');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.querySelector('.chat-section');

    // 띵곰 이미지 URL 정의
    const botIconUrl = '/static/images/swu/thinkbear_head.png';

    chatSendButton.addEventListener('click', async function () {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            // 사용자 메시지 추가
            const userMessageDiv = document.createElement('div');
            userMessageDiv.classList.add('chat-window', 'user-message'); // 올바른 클래스 추가
            userMessageDiv.innerHTML = `<div class="chat-message">${userMessage}</div>`;
            chatWindow.appendChild(userMessageDiv);

            chatInput.value = ''; // 입력창 초기화
            chatWindow.scrollTop = chatWindow.scrollHeight; // 최신 메시지로 스크롤

            // Flask API 요청
            try {
                const response = await fetch('/api/chatbot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userMessage }),
                });

                const data = await response.json();
                if (response.ok) {
                    const botMessageDiv = document.createElement('div');
                    botMessageDiv.classList.add('chat-window', 'bot-message'); // 올바른 클래스 추가
                    botMessageDiv.innerHTML = `
                        <img src="${botIconUrl}" alt="띵곰이" class="bot-icon">
                        <div class="chat-inner-window">
                            <div class="chat-message">${data.response}</div>
                        </div>`;
                    chatWindow.appendChild(botMessageDiv);
                } else {
                    const errorMessageDiv = document.createElement('div');
                    errorMessageDiv.classList.add('chat-window', 'bot-message'); // 오류 메시지도 봇 스타일 적용
                    errorMessageDiv.innerHTML = `
                    <img src="${botIconUrl}" alt="띵곰이" class="bot-icon">
                    <div class="chat-inner-window">
                        <div class="chat-message">오류: ${data.error}</div>
                    </div>`;
                    chatWindow.appendChild(errorMessageDiv);
                }

                chatWindow.scrollTop = chatWindow.scrollHeight; // 최신 메시지로 스크롤
            } catch (error) {
                const errorMessageDiv = document.createElement('div');
                errorMessageDiv.classList.add('chat-window', 'bot-message');
                errorMessageDiv.innerHTML = `<div class="chat-message">서버와 연결할 수 없습니다.</div>`;
                chatWindow.appendChild(errorMessageDiv);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        }
    });
});
