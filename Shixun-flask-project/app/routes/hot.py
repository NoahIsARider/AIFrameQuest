from flask import Blueprint

hot_bp = Blueprint('hot', __name__)

@hot_bp.route('/hot')
def hot():
    return {'message': 'Welcome to hot page'} 