from flask_restful import Api, Resource
from sqlalchemy import Text, JSON
from __init__ import app, db
from sqlalchemy import Column, Integer, String, Text
from sqlite3 import IntegrityError

class Trivia(db.Model):
    __tablename__ = 'trivia'
    id = db.Column(Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f"<Trivia(id={self.id}, question={self.question}, correct_answer={self.correct_answer})>"

    # CRUD methods for Trivia class
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            'id': self.id,
            'question': self.question,
            'correct_answer': self.correct_answer,
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self
        
        question = inputs.get("question", None)
        correct_answer = inputs.get("correct_answer", None)

        if question:
            self.question = question
        if correct_answer:
            self.correct_answer = correct_answer

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        restored_questions = {}

        for question_data in data:  
            question_data.pop('id', None)

            # Check if the question already exists
            existing_question = Trivia.query.filter_by(
                question=question_data.get('question'),
            ).first()

            if existing_question:
                # Update the existing question with new data
                for key, value in question_data.items():
                    setattr(existing_question, key, value)

                try:
                    db.session.commit()
                    restored_questions[existing_question.id] = {
                        'status': 'updated',
                        'food': existing_question.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_questions[existing_question.id] = {
                        'status': 'error',
                        'message': str(e)
                    }
            else:
                # Create a new question
                new_question = Trivia(**question_data)
                db.session.add(new_question)
                try:
                    db.session.commit()
                    restored_questions[new_question.id] = {
                        'status': 'created',
                        'food': new_question.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_questions[new_question.id] = {
                        'status': 'error',
                        'message': str(e)
                    }

        return restored_questions

def initQuestions(): 
    question_data = [
        {
            "question": "What is diabetes?",
            "correct_answer": "b"
        },
        {
            "question": "What does insulin do?",
            "correct_answer": "c"
        },
        {
            "question": "How does healthy eating help with diabetes?",
            "correct_answer": "a"
        },
        {
            "question": "What does exercise do for blood sugar?",
            "correct_answer": "b"
        },
        {
            "question": "What is blood sugar?",
            "correct_answer": "d"
        },
        {
            "question": "Why are doctor visits important for diabetes?",
            "correct_answer": "a"
        },
        {
            "question": "What are symptoms of diabetes?",
            "correct_answer": "c"
        },
        {
            "question": "What does taking care of diabetes involve?",
            "correct_answer": "d"
        },
        {
            "question": "What is glucose?",
            "correct_answer": "b"
        },
        {
            "question": "What does glycemic load measure?",
            "correct_answer": "a"
        },
        {
            "question": "What is the good glucose range before meals?",
            "correct_answer": "c"
        },
        {
            "question": "What is the bad glucose range?",
            "correct_answer": "d"
        },
        {
            "question": "What are carbohydrates?",
            "correct_answer": "a"
        },
        {
            "question": "What might you feel with low blood sugar?",
            "correct_answer": "b"
        },
        {
            "question": "What might you feel with high blood sugar?",
            "correct_answer": "c"
        },
        {
            "question": "What is the finger prick test for?",
            "correct_answer": "b"
        }
    ]
    
    
  
    for question in question_data:
        if not Trivia.query.filter_by(question=question["question"]).first():  # check if question already exists aviods duplicates
            new_question = Trivia(
                question=question["question"],
                correct_answer=question["correct_answer"],
            )
            db.session.add(new_question) 
    
    # commit transaction to the database
    try:
        db.session.commit() 
    except IntegrityError:
        db.session.rollback()  
        print("IntegrityError: Could be a duplicate entry or violation of database constraints.")
    except Exception as e:
        db.session.rollback()  
        print(f"Error: {e}")

with app.app_context():
    db.create_all() 
    initQuestions()