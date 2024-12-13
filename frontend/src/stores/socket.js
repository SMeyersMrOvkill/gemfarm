import { ref } from 'vue'
import { io } from 'socket.io-client'

const socket = io(window.location.origin, {
  transports: ['websocket', 'polling'],
  reconnection: true,
  reconnectionAttempts: 5
})

const isConnected = ref(false)

socket.on('connect', () => {
  console.log('Connected to server')
  isConnected.value = true
})

socket.on('disconnect', () => {
  console.log('Disconnected from server')
  isConnected.value = false
})

export const useSocketStore = () => {
  return {
    socket,
    isConnected
  }
}
