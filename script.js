const predefinedQuestions = [
  "What is my zodiac sign?",
  "Tell me about my birth chart",
  "What does my horoscope say today?",
  "Will I have good luck this year?"
];

const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const predefinedList = document.getElementById("predefined-questions");

// Load predefined questions in sidebar
predefinedQuestions.forEach(q => {
  const li = document.createElement("li");
  li.textContent = q;
  li.addEventListener("click", () => {
    userInput.value = q;
    userInput.focus();
  });
  predefinedList.appendChild(li);
});

// Simple rule-based answers function
function getBotResponse(question) {
  const q = question.toLowerCase();
  if (q.includes("zodiac")) {
    return "To know your zodiac sign, please provide your birth date!";
  }
  if (q.includes("birth chart")) {
    return "Birth charts are a detailed map of the sky at your birth — you can use free sites like astro.com to get yours.";
  }
  if (q.includes("horoscope")) {
    return "Today's horoscope says: good energy is coming your way! Stay positive.";
  }
  if (q.includes("luck")) {
    return "Luck favors the prepared! Keep an open heart and work hard.";
  }
  return "Sorry, I don't have an answer for that question yet.";
}

// Append message to chat window
function appendMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  msgDiv.textContent = text;
  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Handle sending message
sendBtn.addEventListener("click", () => {
  const userText = userInput.value.trim();
  if (!userText) return;

  appendMessage(userText, "user");

  // Simulate bot "thinking"
  setTimeout(() => {
    const botReply = getBotResponse(userText);
    appendMessage(botReply, "bot");
  }, 800);

  userInput.value = "";
});
