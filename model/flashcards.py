from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from __init__ import db

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.String(300), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "term": self.term,
            "definition": self.definition
        }

def initFlashcards():
    # Ensure the table exists
    db.create_all()
    if Flashcard.query.count() == 0:
        sample_cards = [
            Flashcard(term="Diabetes", definition="A condition where the body can't properly use sugar from food."),
            Flashcard(term="Insulin", definition="A hormone that helps sugar get into cells for energy."),
            Flashcard(term="Healthy Eating", definition="Eating fruits, vegetables, and whole grains helps manage diabetes."),
            Flashcard(term="Exercise", definition="Being active helps your body use sugar better."),
            Flashcard(term="Blood Sugar", definition="The amount of sugar in your blood. It should not be too high or low."),
            Flashcard(term="Doctor Visits", definition="Regular check-ups help manage diabetes and stay healthy."),
            Flashcard(term="Symptoms", definition="Feeling tired, thirsty, or needing to go to the bathroom often."),
            Flashcard(term="Taking Care", definition="Eating well, moving more, and taking medicine if needed.")
        ]
        db.session.bulk_save_objects(sample_cards)
        db.session.commit()