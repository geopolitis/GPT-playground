document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const inputBox = document.getElementById('input');
    const chatbox = document.getElementById('chatbox');
    const tokenInfoElement = document.getElementById('token-info');

    const appendMessage = (role, content) => {
        const messageContainer = document.createElement('div');
        messageContainer.className = role === 'user' ? 'user-message' : 'bot-message';

        const nameElement = document.createElement('strong');
        nameElement.textContent = role === 'user' ? 'Me: ' : 'Toula: ';
        messageContainer.appendChild(nameElement);

        const contentElement = document.createElement('span');
        contentElement.textContent = content;
        messageContainer.appendChild(contentElement);

        chatbox.appendChild(messageContainer);
        chatbox.scrollTop = chatbox.scrollHeight;
    };

    const sendMessage = async () => {
        const userInput = inputBox.value.trim();
        if (!userInput) return;
        inputBox.value = '';

        appendMessage('user', userInput);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input: userInput }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            appendMessage('assistant', data.response);
            tokenInfoElement.textContent = data.token_info;

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            appendMessage('assistant', 'An error occurred while processing your message. Please try again.');
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    inputBox.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
