/**
 * Intelligence ( AI ) Interactions
 *
 * Import step 3
 */

// UI event handlers
function sendMessage() {
    const message = messageInput.value;
    if (message && isConnected) {
        socket.emit('message', { message: message });
        addMessage(message, true);
        messageInput.value = '';
    }
}