import base64
from flask import Blueprint, request, jsonify, g
from flask_restful import Api
from flask_login import current_user, login_required
from api.jwt_authorize import token_required
from model.trivia import Trivia
from model.answers import Answers
from __init__ import db

# Define Blueprint and Api
trivia_api = Blueprint('trivia_api', __name__, url_prefix='/api/trivia')
api = Api(trivia_api)

@trivia_api.route('/<int:question_id>', methods=['GET'])
def get_trivia(question_id):
    try:
        # Fetch the question
        question = Trivia.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404

        # Fetch all corresponding answers
        answers = Answers.query.filter_by(trivia_id=question_id).all()

        # Combine and return
        return jsonify({
            'id': question.id,
            'question': question.question,
            'correct_answer': question.correct_answer,
            'answers': [
                {
                    'answer_id': ans.answer_id,
                    'answer': ans.answer
                } for ans in answers
            ]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to fetch trivia with answers', 'message': str(e)}), 500