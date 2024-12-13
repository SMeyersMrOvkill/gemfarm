<template>
  <div class="card-body" id="game-container" ref="gameContainer">
    <!-- P5.js canvas will be mounted here -->
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import p5 from 'p5'

const gameContainer = ref(null)
const player = {
  x: 200,
  y: 200,
  size: 20,
  speed: 3
}

let targetX = player.x
let targetY = player.y
let isMoving = false

const sketch = (p) => {
  p.setup = () => {
    const canvas = p.createCanvas(400, 400)
    canvas.parent(gameContainer.value)
  }

  p.draw = () => {
    p.background(51)
    
    if (isMoving) {
      const dx = targetX - player.x
      const dy = targetY - player.y
      const distance = p.sqrt(dx * dx + dy * dy)
      
      if (distance > 1) {
        player.x += (dx / distance) * player.speed
        player.y += (dy / distance) * player.speed
      } else {
        isMoving = false
        player.x = targetX
        player.y = targetY
      }
    }
    
    p.fill(0, 255, 0)
    p.circle(player.x, player.y, player.size)
  }
}

const movePlayer = (direction) => {
  const moveDistance = 50
  isMoving = true
  
  switch(direction.toLowerCase()) {
    case 'north':
      targetY = Math.max(player.y - moveDistance, player.size/2)
      break
    case 'south':
      targetY = Math.min(player.y + moveDistance, 400 - player.size/2)
      break
    case 'east':
      targetX = Math.min(player.x + moveDistance, 400 - player.size/2)
      break
    case 'west':
      targetX = Math.max(player.x - moveDistance, player.size/2)
      break
  }
}

onMounted(() => {
  new p5(sketch)
  window.movePlayer = movePlayer
})
</script>

<style scoped>
#game-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  background-color: var(--bs-dark-bg-subtle);
}

#game-container canvas {
  max-width: 100%;
  height: auto;
}
</style>
