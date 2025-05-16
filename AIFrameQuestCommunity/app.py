import os
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, session
from utils.faiss_search import process_search_request, initialize_index, IMAGE_FOLDER, UPLOAD_FOLDER
from utils.user_metadata import register_user, login_user, get_image_term, get_term_comments, add_comment, get_all_terms, get_images_by_term

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Routes section begins here

# Routes
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session.get('user'))

@app.route('/search', methods=['POST'])
def search():
    # Check if an image was uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Process the search request using the faiss_search module
    result = process_search_request(file)
    
    # Check if there was an error
    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], dict) and 'error' in result[0]:
        return jsonify(result[0]), result[1]
    
    # Add image terms to the results
    for item in result['results']:
        item['term'] = get_image_term(item['image'])
    
    return jsonify(result)

# User authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        if not nickname or not phone or not password:
            return jsonify({'error': 'Nickname, phone number, and password are required'}), 400
        
        success, message = register_user(nickname, phone, password)
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        if not phone or not password:
            return jsonify({'error': 'Phone number and password are required'}), 400
        
        success, message, nickname, role = login_user(phone, password)
        if success:
            session['user'] = nickname
            session['role'] = role
            
            # Redirect based on user role
            if role == 'admin':
                return jsonify({'message': message, 'redirect': '/admin'}), 200
            else:
                return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html', user=session.get('user'))

# Term routes
@app.route('/term/<term>')
def view_term(term):
    # Get all images for this term
    images = get_images_by_term(term)
    
    # Get comments for this term
    term_data = get_term_comments(term)
    
    return render_template('term.html', term=term, images=images, term_data=term_data, user=session.get('user'))

@app.route('/terms')
def view_all_terms():
    terms = get_all_terms()
    return render_template('terms.html', terms=terms)

@app.route('/add_comment', methods=['POST'])
def add_new_comment():
    if 'user' not in session:
        return jsonify({'error': 'You must be logged in to add a comment'}), 401
    
    term = request.form.get('term')
    comment_text = request.form.get('comment')
    rating = request.form.get('rating')
    
    if not term or not comment_text or not rating:
        return jsonify({'error': 'Term, comment, and rating are required'}), 400
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    except ValueError:
        return jsonify({'error': 'Rating must be a number'}), 400
    
    success, message = add_comment(term, session['user'], comment_text, rating)
    if success:
        return redirect(url_for('view_term', term=term))
    else:
        return jsonify({'error': message}), 500

@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/uploads/<path:filename>')
def get_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # Build the index at startup and keep it in memory
    print("Initializing the index at startup...")
    initialize_index()
    
    app.run(debug=True, host='127.0.0.1', port=5000)