const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

let chatHistory = [];

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const userMessage = userInput.value.trim();
    if (!userMessage) return;
    
    // 顯示用戶的訊息
    appendMessage("user", userMessage);
    userInput.value = "";

    try {
        // 發送請求到後端
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: userMessage, history: chatHistory }),
        });

        if (!response.ok) {
            throw new Error("Failed to get response from server.");
        }

        const data = await response.json();
        const botMessage = data.answer;

        // 顯示機器人的回應
        appendMessage("bot", botMessage);

        // 更新聊天歷史
        chatHistory.push(`User: ${userMessage}`);
        chatHistory.push(`Assistant: ${botMessage}`);
    } catch (error) {
        console.error(error);
        appendMessage("bot", "Error: Unable to connect to the server.");
    }
});

function appendMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
