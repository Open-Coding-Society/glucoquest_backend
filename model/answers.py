from flask_restful import Api, Resource
from sqlalchemy import Text, JSON
from __init__ import app, db
from sqlalchemy import Column, Integer, String, Text
from sqlite3 import IntegrityError

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c', 'd'
    answer = db.Column(db.String, nullable=False)
    trivia_id = db.Column(db.Integer, db.ForeignKey('trivia.id'), nullable=False)

    def __repr__(self):
        return f"<Answers(id={self.id}, answer_id={self.answer_id}, answer={self.answer}, trivia_id={self.trivia_id})>"

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
            'answer_id': self.answer_id,
            'answer': self.answer,
            'trivia_id': self.trivia_id,
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self
        
        answer_id = inputs.get("answer_id", None)
        answer = inputs.get("answer", None)
        trivia_id = inputs.get("trivia_id", None)

        if answer_id:
            self.question = answer_id
        if answer:
            self.answer = answer
        if trivia_id:
            self.trivia_id = trivia_id

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
        restored_answers = {}

        for answer_data in data:  
            answer_data.pop('id', None)

            # Check if the answer already exists
            existing_answer = Answers.query.filter_by(
                answer=answer_data.get('answer'),
            ).first()

            if existing_answer:
                # Update the existing answer with new data
                for key, value in answer_data.items():
                    setattr(existing_answer, key, value)

                try:
                    db.session.commit()
                    restored_answers[existing_answer.id] = {
                        'status': 'updated',
                        'food': existing_answer.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_answers[existing_answer.id] = {
                        'status': 'error',
                        'message': str(e)
                    }
            else:
                # Create a new question
                new_answer = Answers(**answer_data)
                db.session.add(new_answer)
                try:
                    db.session.commit()
                    restored_answers[new_answer.id] = {
                        'status': 'created',
                        'food': new_answer.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_answers[new_answer.id] = {
                        'status': 'error',
                        'message': str(e)
                    }

        return restored_answers

def initAnswers(): 
    answer_data = [
        {
            "answer_id": "a",
            "answer": "Sample text here",
            "trivia_id": 1,
        },
        {
            "answer_id": "b",
            "answer": "Sample text here2",
            "trivia_id": 1,
        },
    ]       
    
  
    for answer in answer_data:
        if not Answers.query.filter_by(answer=answer["answer"]).first():  # check if answer already exists aviods duplicates
            new_answer = Answers(
                answer_id=answer["answer_id"],
                answer=answer["answer"],
                trivia_id=answer["trivia_id"],
            )
            db.session.add(new_answer) 
    
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
    initAnswers()