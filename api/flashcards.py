from flask import Blueprint, jsonify, request, current_app
from flask_restful import Api
from model.flashcards import db, Flashcard
import difflib 

# Blueprint for the flashcards API
flashcards_api = Blueprint('flashcards_api', __name__, url_prefix='/api')
api = Api(flashcards_api)

# GET endpoint to retrieve all flashcards from the database
@flashcards_api.route('/flashcards', methods=['GET'])
def get_flashcards():
    # Query all flashcards from the database
    flashcards = Flashcard.query.all()
    # Return a JSON list of all flashcards using their to_dict() method
    return jsonify([card.to_dict() for card in flashcards])

# POST endpoint to add a new flashcard to the database
@flashcards_api.route('/flashcards', methods=['POST'])
def add_flashcard():
    # Search the incoming JSON request for 'term' and 'definition'
    data = request.get_json()
    new_card = Flashcard(term=data['term'], definition=data['definition']) # Create a new Flashcard object
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.to_dict()), 201

# DELETE endpoint to remove a flashcard by its ID
@flashcards_api.route('/flashcards/<int:id>', methods=['DELETE'])
def delete_flashcard(id):
    # Query for the flashcard by ID, or return 404 if not found
    card = Flashcard.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Deleted successfully."})

@flashcards_api.route('/flashcards/grade', methods=['POST'])
def grade_flashcards():
    """
    Expects JSON:
    {
        "answers": [
            {"user_answer": "prick test", "correct_term": "Finger Prick Test"},
            ...
        ]
    }
    Returns JSON:
    {
        "results": [
            {"user_answer": "...", "correct_term": "...", "is_correct": true/false, "similarity": 0.85},
            ...
        ]
    }
    """
    data = request.get_json()
    answers = data.get("answers", [])
    results = []
    for ans in answers:
        user = ans.get("user_answer", "").strip().lower()
        correct = ans.get("correct_term", "").strip().lower()
        # Use difflib to get similarity ratio
        similarity = difflib.SequenceMatcher(None, user, correct).ratio()
        # Accept if similarity is 0.7 or higher, or if user answer is a substring of correct answer
        is_correct = similarity >= 0.7 or user in correct or correct in user
        results.append({
            "user_answer": ans.get("user_answer", ""),
            "correct_term": ans.get("correct_term", ""),
            "is_correct": is_correct,
            "similarity": similarity
        })
    return jsonify({"results": results})