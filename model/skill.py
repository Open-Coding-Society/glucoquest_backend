# skill.py

from __init__ import db
from flask import jsonify, request
from model.user import User  # Assuming this is needed for valid user references
from sqlalchemy.exc import IntegrityError

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    expertise_level = db.Column(db.String(50), nullable=False)  # e.g., Beginner, Intermediate, Advanced

    def __init__(self, user_id, skill_name, expertise_level):
        self.user_id = user_id
        self.skill_name = skill_name
        self.expertise_level = expertise_level

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_name': self.skill_name,
            'expertise_level': self.expertise_level,
        }

    @staticmethod
    def init_skills():
        """Initialize the skill table with sample data."""
        sample_skills = [
            {"user_id": 1, "skill_name": "Python", "expertise_level": "Advanced"},
            {"user_id": 2, "skill_name": "Java", "expertise_level": "Intermediate"},
            {"user_id": 3, "skill_name": "React", "expertise_level": "Beginner"},
            {"user_id": 4, "skill_name": "Machine Learning", "expertise_level": "Advanced"}
        ]
        for sample in sample_skills:
            try:
                skill = Skill(
                    user_id=sample["user_id"],
                    skill_name=sample["skill_name"],
                    expertise_level=sample["expertise_level"]
                )
                db.session.add(skill)
            except Exception as e:
                db.session.rollback()
                print(f"Error adding skill: {e}")
        db.session.commit()

    @staticmethod
    def restore(data):
        """Restore skill entries from JSON data."""
        for entry in data:
            try:
                skill = Skill(
                    user_id=entry['user_id'],
                    skill_name=entry['skill_name'],
                    expertise_level=entry['expertise_level']
                )
                db.session.add(skill)
            except IntegrityError:
                db.session.rollback()
        db.session.commit()
