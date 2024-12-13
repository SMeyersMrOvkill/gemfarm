document.addEventListener('DOMContentLoaded', function() {
    // Initialize socket with explicit URL and options
    const socket = io(window.location.origin, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: 5
    });
    
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');

    let isConnected = false;

    function updateConnectionStatus(connected) {
        isConnected = connected;
        statusDot.classList.toggle('connected', connected);
        statusText.textContent = connected ? 'Connected' : 'Disconnected';
        sendButton.disabled = !connected;
        messageInput.disabled = !connected;
    }

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addErrorMessage(content) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = content;
        chatMessages.appendChild(errorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Socket event handlers
    socket.on('connect', () => {
        console.log('Connected to server');
        updateConnectionStatus(true);
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        updateConnectionStatus(false);
    });

    socket.on('response', (data) => {
        addMessage(data.message);
        
        // Check if there's a move command
        if (data.movement) {
            movePlayer(data.movement);
        }
    });

    socket.on('error', (data) => {
        addErrorMessage(data.message);
    });

    // Send message function
    function sendMessage() {
        if (!isConnected || !messageInput.value.trim()) return;
        
        const message = messageInput.value.trim();
        socket.emit('message', { message: message });
        addMessage(message, true);
        messageInput.value = '';
    }

    // Event listeners for sending messages
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initialize UI state
    updateConnectionStatus(false);
});
