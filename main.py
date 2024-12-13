import os
from gemfarm import create_app
from flask import socketio

# Get environment setting from ENV var, default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = env == 'development'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
