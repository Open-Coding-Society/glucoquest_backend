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

def initFlashcards(csv_path='flashcards.csv'):
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