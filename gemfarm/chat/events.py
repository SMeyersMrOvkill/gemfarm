import logging
from flask import request
from flask_socketio import emit
from gemfarm import socketio
from gemfarm.chat.ai import get_ai_response
from gemfarm.utils import check_rate_limit
from collections import defaultdict
import threading

# Configure logging
logger = logging.getLogger(__name__)

# Rate limiting
request_counts = defaultdict(list)
rate_limit_lock = threading.Lock()

@socketio.on('connect')
def handle_connect(auth):
    """Handle client connection"""
    logger.info(f'Client connected: {request.sid}')
    emit('connection_status', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f'Client disconnected: {request.sid}')

@socketio.on('message')
def handle_message(data):
    """Handle incoming messages and generate responses using AI"""
    if not isinstance(data, dict) or 'message' not in data:
        emit('error', {'message': 'Invalid message format'})
        return

    client_id = request.sid

    if not check_rate_limit(client_id, request_counts, rate_limit_lock):
        emit('error', {
            'message': 'Rate limit exceeded. Please wait before sending more requests.'
        })
        return

    try:
        user_input = data.get('message', '')
        logger.debug(f'Received message from {client_id}: {user_input}')
        
        response = get_ai_response(user_input)
        emit('response', response)
            
    except Exception as e:
        logger.error(f'Error processing message: {str(e)}')
        emit('error', {'message': 'An error occurred while processing your request.'})
