let player = {
    x: 200,
    y: 200,
    size: 20,
    speed: 3
};

// Initialize movements
let targetX = player.x;
let targetY = player.y;
let isMoving = false;

function setup() {
    // Create canvas inside the game-container
    const container = document.getElementById('game-container');
    const canvas = createCanvas(400, 400);
    canvas.parent(container);
}

function draw() {
    background(51); // Dark background
    
    // Update player position
    if (isMoving) {
        let dx = targetX - player.x;
        let dy = targetY - player.y;
        let distance = sqrt(dx * dx + dy * dy);
        
        if (distance > 1) {
            player.x += (dx / distance) * player.speed;
            player.y += (dy / distance) * player.speed;
        } else {
            isMoving = false;
            player.x = targetX;
            player.y = targetY;
        }
    }
    
    // Draw player
    fill(0, 255, 0);
    circle(player.x, player.y, player.size);
}

// Function to move player based on direction
function movePlayer(direction) {
    const moveDistance = 50; // Distance to move in pixels
    isMoving = true;
    
    switch(direction.toLowerCase()) {
        case 'north':
            targetY = max(player.y - moveDistance, player.size/2);
            break;
        case 'south':
            targetY = min(player.y + moveDistance, height - player.size/2);
            break;
        case 'east':
            targetX = min(player.x + moveDistance, width - player.size/2);
            break;
        case 'west':
            targetX = max(player.x - moveDistance, player.size/2);
            break;
    }
}

// Make movePlayer function globally accessible
window.movePlayer = movePlayer;
