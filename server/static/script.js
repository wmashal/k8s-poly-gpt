const chatLog = document.getElementById('chat-log');
const form = document.getElementById('chat-form');
const progressBar = document.getElementById('progress-bar');
const messageInput = document.getElementById('message');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = messageInput.value;
    appendMessage("You", message);
    messageInput.value = '';
    sendMessage(message);
});

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender === "You" ? 'user-message' : 'bot-message');
    const codeBlockRegex = /`([a-z]+)?\n([\s\S]*?)`/;
    const match = message.match(codeBlockRegex);
    // Check if the message contains a code block, YAML, or Bash
    if (message.indexOf("```") > -1) {
        const language = match[1] || ''; // Extract language (if specified)
        const codeContent = match[2].trim(); // Extract code content

        const preElement = document.createElement('pre');
        const codeElement = document.createElement('code');

        // Use Prism to highlight the code if the language is supported
        if (Prism.languages[language]) {
            codeElement.classList.add(`language-${language}`);

            codeElement.textContent = codeContent;
            Prism.highlightElement(codeElement); // Apply syntax highlighting
        } else {
            // If language is not supported, display the code as plain text
            codeElement.textContent = message;
        }

        preElement.appendChild(codeElement);
        messageElement.appendChild(preElement);
    } else {
        // If it's not a code block, display the message normally
        messageElement.textContent = `${sender}: ${message}`;
    }

    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll
}

function sendMessage(message) {
    progressBar.style.display = 'block';

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
        .then(response => response.json())
        .then(data => {
            appendMessage("K8s Poly GPT", data.response);
            progressBar.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage("K8s Poly GPT", "An error occurred. Please try again.");
            progressBar.style.display = 'none';
        });
}
