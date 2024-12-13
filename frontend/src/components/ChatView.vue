<template>
  <div class="card-body d-flex flex-column">
    <div id="chat-messages" class="chat-container flex-grow-1 mb-3">
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="['message', message.isUser ? 'user-message' : 'bot-message']">
        {{ message.content }}
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
    <div class="input-group">
      <input 
        type="text" 
        v-model="messageInput"
        :disabled="!isConnected"
        class="form-control" 
        placeholder="Type your message..."
        @keypress.enter="sendMessage"
      >
      <button 
        class="btn btn-secondary" 
        :disabled="!isConnected"
        @click="sendMessage"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { io } from 'socket.io-client'
import { useSocketStore } from '../stores/socket'

const socketStore = useSocketStore()
const messages = ref([])
const messageInput = ref('')
const error = ref('')

const sendMessage = () => {
  const message = messageInput.value.trim()
  if (message && socketStore.isConnected) {
    socketStore.socket.emit('message', { message })
    messages.value.push({ content: message, isUser: true })
    messageInput.value = ''
  }
}

onMounted(() => {
  socketStore.socket.on('response', (data) => {
    messages.value.push({ content: data.message, isUser: false })
    if (data.movement) {
      window.movePlayer(data.movement)
    }
  })

  socketStore.socket.on('error', (data) => {
    error.value = data.message
  })
})
</script>

<style scoped>
.chat-container {
  height: 400px;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
}

.user-message {
  background-color: var(--bs-secondary-bg);
  margin-left: 2rem;
}

.bot-message {
  background-color: var(--bs-dark-bg-subtle);
  margin-right: 2rem;
}

.error-message {
  color: var(--bs-danger);
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  background-color: var(--bs-danger-bg-subtle);
}
</style>
