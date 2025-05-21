from flask import Blueprint, request, jsonify
from datetime import datetime
from __init__ import db

# Model for leaderboard entries
class MatchingLeaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    time = db.Column(db.Integer, nullable=False)  # seconds
    date = db.Column(db.String(16), nullable=False)  # e.g., '2024-06-01'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'date': self.date
        }

# Blueprint for matching game API
matching_api = Blueprint('matching_api', __name__)

@matching_api.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    entries = MatchingLeaderboard.query.order_by(MatchingLeaderboard.time.asc()).limit(20).all()
    return jsonify([entry.to_dict() for entry in entries])

@matching_api.route('/api/leaderboard', methods=['POST'])
def add_leaderboard_entry():
    data = request.get_json()
    name = data.get('name', 'Anonymous').strip()[:64]
    time = int(data.get('time', 0))
    date = data.get('date') or datetime.utcnow().strftime('%Y-%m-%d')
    entry = MatchingLeaderboard(name=name, time=time, date=date)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201

# Create the table if it doesn't exist
def init_matching_leaderboard():
    db.create_all()