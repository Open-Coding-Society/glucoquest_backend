from flask import Blueprint, request, jsonify
from flask_restful import Api
from datetime import datetime, timezone
from __init__ import db

# Define Blueprint and Api
racing_api = Blueprint('racing_api', __name__, url_prefix='/api/racing')
api = Api(racing_api)

# Model for leaderboard entries
class RacingLeaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Integer, nullable=False) 
    date = db.Column(db.String(16), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score,
            'date': self.date
        }

@racing_api.route('', methods=['GET'])
def get_leaderboard():
    entries = RacingLeaderboard.query.order_by(RacingLeaderboard.score.asc()).limit(20).all()
    return jsonify([entry.to_dict() for entry in entries])

@racing_api.route('', methods=['POST'])
def add_leaderboard_entry():
    data = request.get_json()
    name = data.get('name', 'Anonymous').strip()[:64]
    score = int(data.get('score', 0))
    date = data.get('date') or datetime.now(timezone('US/Pacific')).strftime('%Y-%m-%d')
    entry = RacingLeaderboard(name=name, score=score, date=date)
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201


def init_racing_leaderboard():
    db.create_all()