<template>
  <div class="connection-status">
    <span :class="['status-dot', { connected: isConnected }]"></span>
    <span class="status-text">{{ isConnected ? 'Connected' : 'Disconnected' }}</span>
  </div>
</template>

<script setup>
import { useSocketStore } from '../stores/socket'

const socketStore = useSocketStore()
const { isConnected } = socketStore
</script>

<style scoped>
.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--bs-danger);
}

.status-dot.connected {
  background-color: var(--bs-success);
}
</style>
