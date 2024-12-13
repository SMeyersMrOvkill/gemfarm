<template>
  <div class="container-fluid py-4">
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Game View</h5>
          </div>
          <GameView />
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Gemini Chat</h5>
            <ConnectionStatus />
          </div>
          <ChatView />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import GameView from './components/GameView.vue'
import ChatView from './components/ChatView.vue'
import ConnectionStatus from './components/ConnectionStatus.vue'
</script>

<style>
@import './assets/custom.css';
</style>
