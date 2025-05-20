from flask import Blueprint, jsonify, request, current_app
from flask_restful import Api
from model.flashcards import db, Flashcard

flashcards_api = Blueprint('flashcards_api', __name__, url_prefix='/api')
api = Api(flashcards_api)

@flashcards_api.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = Flashcard.query.all()
    return jsonify([card.to_dict() for card in flashcards])

@flashcards_api.route('/flashcards', methods=['POST'])
def add_flashcard():
    data = request.get_json()
    new_card = Flashcard(term=data['term'], definition=data['definition'])
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.to_dict()), 201

@flashcards_api.route('/flashcards/<int:id>', methods=['DELETE'])
def delete_flashcard(id):
    card = Flashcard.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Deleted successfully."})