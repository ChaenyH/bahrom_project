document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.getElementById("uploadReceipt");
    uploadButton.addEventListener("click", function () {
        alert("영수증 업로드 기능은 준비 중입니다!");
    });
});

document.querySelector("#chatbotButton").addEventListener("click", function () {
    const message = document.querySelector("#chatInput").value;
    fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
    })
        .then((res) => res.json())
        .then((data) => {
            alert("챗봇 응답: " + data.response);
        });
});
