import json
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover = db.Column(db.String(255))
    type = db.Column(db.String(50))
    views = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    images = db.relationship('Image', backref='post', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": json.loads(self.description) if self.description else [],
            "cover": self.cover,
            "type": self.type,
            "views": self.views,
            "comments": [c.to_dict() for c in self.comments],
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    date = db.Column(db.Date)

    def to_dict(self):
        return {
             "id": self.id,
            "name": self.name,
            "text": self.text,
            "rating": self.rating or 0,
            "date": self.date.isoformat() if self.date else None
        }


class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    entry = db.Column(db.String(50))  # 如 "entry1"
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "entry": self.entry,
            "post_id": self.post_id
        }


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='user')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }


class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.String(20), primary_key=True)  # 管理员ID，如 "20250527001"
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='admin')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }