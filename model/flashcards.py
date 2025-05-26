import csv
import os
from __init__ import db

class Flashcard(db.Model):
    __tablename__ = 'flashcards'  # Explicitly name the table
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each flashcard
    term = db.Column(db.String(100), nullable=False)  # The term or question
    definition = db.Column(db.String(300), nullable=False)  # The answer or definition

    def to_dict(self):
        # Convert the Flashcard object to a dictionary for easy JSON serialization
        return {
            "id": self.id,
            "term": self.term,
            "definition": self.definition
        }

def initFlashcards(csv_path='instance/volumes/flashcards.csv'):
    print("Flashcards loaded!")
    db.create_all()
    # Read flashcards from CSV and add them if not already present
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if the term already exists to avoid duplicates
                if not Flashcard.query.filter_by(term=row['term']).first():
                    card = Flashcard(term=row['term'], definition=row['definition'])
                    db.session.add(card)
            db.session.commit()
'''
def initFlashcards():
    # Ensure the flashcards table exists in the database
    db.create_all()
    # Only add sample data if the table is empty
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
        # Bulk insert all sample flashcards into the database
        db.session.bulk_save_objects(sample_cards)
        db.session.commit()
'''