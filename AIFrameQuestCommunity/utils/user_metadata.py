import os
import json
from flask import session

# Configuration
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
USERS_FILE = os.path.join(DATA_FOLDER, 'users.json')
METADATA_FILE = os.path.join(DATA_FOLDER, 'image_metadata.json')
COMMENTS_FILE = os.path.join(DATA_FOLDER, 'comments.json')

# Ensure data directory exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# User authentication functions
def load_users():
    """Load users from the JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)['users']
        return []
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

def save_users(users):
    """Save users to the JSON file"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"users": users}, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def register_user(nickname, phone, password):
    """Register a new user"""
    users = load_users()
    
    # Check if nickname already exists
    if any(user['nickname'] == nickname for user in users):
        return False, "Nickname already exists"
    
    # Check if phone already exists
    if any(user['phone'] == phone for user in users):
        return False, "Phone number already exists"
    
    # Add new user with 'user' role
    users.append({
        "nickname": nickname,
        "phone": phone,
        "password": password,
        "role": "user"
    })
    
    # Save updated users list
    if save_users(users):
        return True, "Registration successful"
    else:
        return False, "Error saving user data"

def login_user(phone, password):
    """Login a user"""
    users = load_users()
    
    # Find user with matching phone and password
    for user in users:
        if user['phone'] == phone and user['password'] == password:
            return True, "Login successful", user['nickname'], user['role']
    
    return False, "Invalid phone number or password", None, None

# Image metadata functions
def load_metadata():
    """Load image metadata from the JSON file"""
    try:
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)['metadata']
        return {}
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return {}

def get_image_term(image_filename):
    """Get the term/value for an image"""
    metadata = load_metadata()
    return metadata.get(image_filename, "Unknown")

# Comments and ratings functions
def load_comments():
    """Load comments from the JSON file"""
    try:
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)['comments']
        return {}
    except Exception as e:
        print(f"Error loading comments: {e}")
        return {}

def save_comments(comments):
    """Save comments to the JSON file"""
    try:
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"comments": comments}, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving comments: {e}")
        return False

def add_comment(term, nickname, comment, rating):
    """Add a comment and rating for a term"""
    comments = load_comments()
    
    # Initialize term entry if it doesn't exist
    if term not in comments:
        comments[term] = {
            "comments": [],
            "average_rating": 0
        }
    
    # Add new comment
    comments[term]["comments"].append({
        "nickname": nickname,
        "comment": comment,
        "rating": rating
    })
    
    # Update average rating
    total_rating = sum(item["rating"] for item in comments[term]["comments"])
    comments[term]["average_rating"] = total_rating / len(comments[term]["comments"])
    
    # Save updated comments
    if save_comments(comments):
        return True, "Comment added successfully"
    else:
        return False, "Error saving comment"

def get_term_comments(term):
    """Get all comments for a term"""
    comments = load_comments()
    return comments.get(term, {"comments": [], "average_rating": 0})

# Get all unique terms from metadata
def get_all_terms():
    """Get all unique terms from the metadata"""
    metadata = load_metadata()
    return list(set(metadata.values()))

# Get all images for a specific term
def get_images_by_term(term):
    """Get all images that match a specific term"""
    metadata = load_metadata()
    return [filename for filename, value in metadata.items() if value == term]