// Display greeting based on local time
window.onload = function() {
    const greeting = document.getElementById("greeting-msg");
    const hour = new Date().getHours();
    if(hour < 12) greeting.textContent = "Good morning! How can I help you today?";
    else if(hour < 18) greeting.textContent = "Good afternoon! How can I help you today?";
    else greeting.textContent = "Good evening! How can I help you today?";
}

function checkEnter(e) {
    if (e.key === "Enter") sendMessage();
}

function sendMessage() {
    let msgInput = document.getElementById("userInput");
    let msg = msgInput.value;
    if (!msg.trim()) return;

    // Remove greeting message if present
    const greeting = document.getElementById("greeting-msg");
    if (greeting) {
        greeting.remove();
        document.getElementById("chatlog").style.justifyContent = "flex-start";
        document.getElementById("chatlog").style.alignItems = "flex-start";
    }

    let chatlog = document.getElementById("chatlog");
    chatlog.innerHTML += `<div class="message user-msg">💁 You: ${msg}</div>`;

    fetch("/get", {
        method: "POST",
        body: new URLSearchParams({"msg": msg})
    })
    .then(response => response.json())
    .then(data => {
        chatlog.innerHTML += `<div class="message bot-msg">🤖 Karen: ${data.response}</div>`;
        msgInput.value = "";
        chatlog.scrollTop = chatlog.scrollHeight;
    });
}