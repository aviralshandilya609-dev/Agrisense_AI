const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");


// =========================
// SEND MESSAGE
// =========================

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    // Add user's message
    addMessage(message, "user");

    // Clear input
    userInput.value = "";

    // Reset textarea height
    userInput.style.height = "auto";

    // Show typing indicator
    const typingElement = showTyping();

    // Disable send button
    sendButton.disabled = true;

    try {

    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message,
            history: []
        })
    });

    const data = await response.json();

    removeTyping(typingElement);

    addMessage(data.response, "bot");
    if (voiceInputUsed) {
    speakAnswer(data.response);
    voiceInputUsed = false;
}
}
     catch (error) {

        removeTyping(typingElement);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

        console.error("Chatbot error:", error);

    } finally {

        sendButton.disabled = false;

        userInput.focus();
    }
}


// =========================
// ADD MESSAGE
// =========================

function addMessage(message, sender) {

    const messageWrapper = document.createElement("div");

    messageWrapper.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "bot-message"
    );

    if (sender === "bot") {

        messageWrapper.innerHTML = `
            <div class="message-avatar">
                AI
            </div>

            <div class="message-content">

                <div class="message-name">
                    AgriSense AI
                </div>

                <div class="message-bubble">
                    ${formatMessage(message)}
                </div>

                <button class="listen-button" type="button">
                    🔊 Listen
                </button>

            </div>
        `;

        const listenButton =
            messageWrapper.querySelector(".listen-button");

        listenButton.onclick = function () {

            if (window.speechSynthesis.speaking) {

                window.speechSynthesis.cancel();
                this.textContent = "🔊 Listen";

            } else {

                speakAnswer(message);
                this.textContent = "⏹ Stop";
            }
        };

    } else {

        messageWrapper.innerHTML = `
            <div class="message-content">

                <div class="message-bubble">
                    ${formatMessage(message)}
                </div>

            </div>
        `;
    }

    chatArea.appendChild(messageWrapper);

    scrollToBottom();
}

// =========================
// FORMAT MESSAGE
// =========================

function formatMessage(message) {

    return message
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "<br>");
}


// =========================
// TYPING INDICATOR
// =========================

function showTyping() {

    const typingWrapper = document.createElement("div");

    typingWrapper.classList.add(
        "message",
        "bot-message"
    );

    typingWrapper.innerHTML = `
        <div class="message-avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                AgriSense AI
            </div>

            <div class="message-bubble typing-bubble">

                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>

            </div>

        </div>
    `;

    chatArea.appendChild(typingWrapper);

    scrollToBottom();

    return typingWrapper;
}


// =========================
// REMOVE TYPING
// =========================

function removeTyping(element) {

    if (element && element.parentNode) {
        element.parentNode.removeChild(element);
    }
}


// =========================
// SUGGESTION BUTTON
// =========================

function sendSuggestion(text) {

    userInput.value = text;

    sendMessage();
}


// =========================
// ENTER KEY
// =========================

function handleKeyDown(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
}


// =========================
// AUTO RESIZE TEXTAREA
// =========================

userInput.addEventListener("input", function () {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 120) + "px";

});


// =========================
// SCROLL TO BOTTOM
// =========================

function scrollToBottom() {

    chatArea.scrollTop = chatArea.scrollHeight;
}


// =========================
// DELAY
// =========================

function delay(milliseconds) {

    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}
// =========================
// VOICE INPUT
// =========================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition;
let voiceInputUsed = false;

if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.maxAlternatives = 5;
    recognition.interimResults = false;
    recognition.lang = "en-IN";

    recognition.onstart = function () {
    voiceInputUsed = true;

    document.getElementById("voiceButton")
        .classList.add("listening");
};
    recognition.onresult = function (event) {

        const transcript =
            event.results[0][0].transcript;

        userInput.value = transcript;

        userInput.dispatchEvent(new Event("input"));

        document.getElementById("voiceButton")
            .classList.remove("listening");
    };

    recognition.onerror = function (event) {

        console.error("Voice input error:", event.error);

        document.getElementById("voiceButton")
            .classList.remove("listening");
    };

    recognition.onend = function () {

        document.getElementById("voiceButton")
            .classList.remove("listening");
    };

} else {

    console.warn("Speech recognition is not supported in this browser.");
}


// =========================
// START VOICE INPUT
// =========================

function startVoiceInput() {

    if (!recognition) {
        alert("Voice input is not supported in this browser.");
        return;
    }

    recognition.start();
}
// =========================
// TEXT TO SPEECH
// =========================

function speakAnswer(text) {
    if (!("speechSynthesis" in window)) {
        console.warn("Text-to-speech is not supported.");
        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-IN";
    speech.rate = 0.95;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}