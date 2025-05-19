from flask import Flask, request, jsonify, render_template, Blueprint
from datetime import datetime
from __init__ import app, db

# Feedback Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accuracy = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, accuracy, comment):
        self.accuracy = accuracy
        self.comment = comment

    def to_dict(self):
        return {
            'id': self.id,
            'accuracy': self.accuracy,
            'comment': self.comment,
            'timestamp': self.timestamp.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()


# API Endpoints
# filepath: /home/qixiang/nighthawk/dexcom_backend/api/crossword.py
crossword_api = Blueprint('crossword_api', __name__)

@crossword_api.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    if not data or 'accuracy' not in data or not data.get('comment', '').strip():
        return jsonify({'error': 'Missing accuracy or comment'}), 400
    
    feedback = Feedback(accuracy=data['accuracy'], comment=data['comment'].strip())
    db.session.add(feedback)
    db.session.commit()
    return jsonify(feedback.to_dict()), 201

@crossword_api.route('/api/feedback', methods=['GET'])
def get_feedback():
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    return jsonify([f.to_dict() for f in feedbacks])

# @crossword_api.route('/')
# def index():
#     return render_template('crossword.html')
