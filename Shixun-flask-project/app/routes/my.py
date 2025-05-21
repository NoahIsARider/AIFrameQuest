from flask import Blueprint

my_bp = Blueprint('my', __name__)

@my_bp.route('/my')
def my():
    return {'message': 'Welcome to my page'} 