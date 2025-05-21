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
            Flashcard(term="Taking Care", definition="Eating well, moving more, and taking medicine if needed."),
            Flashcard(term="Glucose", definition="A type of sugar your body uses for energy."),
            Flashcard(term="Glycemic Load", definition="How much a food raises your blood sugar after you eat it."),
            Flashcard(term="Good Glucose Range", definition="The healthy amount of sugar in your blood, usually between 80 and 130 before meals."),
            Flashcard(term="Bad Glucose Range", definition="When your blood sugar is too high or too low, which can make you feel sick."),
            Flashcard(term="Carbohydrates", definition="Foods like bread, rice, and fruit that turn into sugar in your body."),
            Flashcard(term="Low Blood Sugar", definition="When there’s not enough sugar in your blood, you might feel shaky or dizzy."),
            Flashcard(term="High Blood Sugar", definition="When there’s too much sugar in your blood, you might feel thirsty or tired."),
            Flashcard(term="Finger Prick Test", definition="A tiny poke on your finger to check your blood sugar.")
        ]
        db.session.bulk_save_objects(sample_cards)
        db.session.commit()