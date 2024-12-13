from flask import render_template, send_from_directory, current_app
from gemfarm.game import bp
import os

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    if path and os.path.exists(os.path.join(current_app.static_folder, 'dist', path)):
        return send_from_directory(os.path.join(current_app.static_folder, 'dist'), path)
    return render_template('index.html')
