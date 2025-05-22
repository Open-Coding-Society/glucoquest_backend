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
            "answer": "A type of exercise",
            "trivia_id": 1
        },
        {
            "answer_id": "b",
            "answer": "A condition where the body can't properly use sugar from food",
            "trivia_id": 1
        },
        {
            "answer_id": "c",
            "answer": "A type of vitamin",
            "trivia_id": 1
        },
        {
            "answer_id": "d",
            "answer": "A type of diet",
            "trivia_id": 1
        },

        {
            "answer_id": "a",
            "answer": "Makes your bones stronger",
            "trivia_id": 2
        },
        {
            "answer_id": "b",
            "answer": "Helps sugar get into cells for energy",
            "trivia_id": 2
        },
        {
            "answer_id": "c",
            "answer": "Helps you sleep better",
            "trivia_id": 2
        },
        {
            "answer_id": "d",
            "answer": "Breaks down fat in your body",
            "trivia_id": 2
        },

        {
            "answer_id": "a",
            "answer": "It makes you gain weight",
            "trivia_id": 3
        },
        {
            "answer_id": "b",
            "answer": "It reduces the need to exercise",
            "trivia_id": 3
        },
        {
            "answer_id": "c",
            "answer": "It helps manage diabetes by choosing good foods",
            "trivia_id": 3
        },
        {
            "answer_id": "d",
            "answer": "It increases blood sugar",
            "trivia_id": 3
        },

        {
            "answer_id": "a",
            "answer": "It makes you eat more sugar",
            "trivia_id": 4
        },
        {
            "answer_id": "b",
            "answer": "It helps your body use sugar better",
            "trivia_id": 4
        },
        {
            "answer_id": "c",
            "answer": "It increases sugar levels",
            "trivia_id": 4
        },
        {
            "answer_id": "d",
            "answer": "It stops insulin from working",
            "trivia_id": 4
        },

        {
            "answer_id": "a",
            "answer": "Sugar in your food",
            "trivia_id": 5
        },
        {
            "answer_id": "b",
            "answer": "The amount of sugar in your blood",
            "trivia_id": 5
        },
        {
            "answer_id": "c",
            "answer": "Sugar in your muscles",
            "trivia_id": 5
        },
        {
            "answer_id": "d",
            "answer": "A sugar pill",
            "trivia_id": 5
        },

        {
            "answer_id": "a",
            "answer": "To get new glasses",
            "trivia_id": 6
        },
        {
            "answer_id": "b",
            "answer": "To stay home from work",
            "trivia_id": 6
        },
        {
            "answer_id": "c",
            "answer": "To manage diabetes and stay healthy",
            "trivia_id": 6
        },
        {
            "answer_id": "d",
            "answer": "To avoid taking medicine",
            "trivia_id": 6
        },

        {
            "answer_id": "a",
            "answer": "Feeling very tired or thirsty",
            "trivia_id": 7
        },
        {
            "answer_id": "b",
            "answer": "Having a fever",
            "trivia_id": 7
        },
        {
            "answer_id": "c",
            "answer": "Hearing loss",
            "trivia_id": 7
        },
        {
            "answer_id": "d",
            "answer": "Itchy skin",
            "trivia_id": 7
        },

        {
            "answer_id": "a",
            "answer": "Skipping meals",
            "trivia_id": 8
        },
        {
            "answer_id": "b",
            "answer": "Taking naps",
            "trivia_id": 8
        },
        {
            "answer_id": "c",
            "answer": "Eating well, moving more, and taking medicine if needed",
            "trivia_id": 8
        },
        {
            "answer_id": "d",
            "answer": "Staying up late",
            "trivia_id": 8
        },

        {
            "answer_id": "a",
            "answer": "A type of fat",
            "trivia_id": 9
        },
        {
            "answer_id": "b",
            "answer": "A type of sugar your body uses for energy",
            "trivia_id": 9
        },
        {
            "answer_id": "c",
            "answer": "A kind of medicine",
            "trivia_id": 9
        },
        {
            "answer_id": "d",
            "answer": "A vitamin",
            "trivia_id": 9
        },

        {
            "answer_id": "a",
            "answer": "How much a food raises your blood sugar after eating",
            "trivia_id": 10
        },
        {
            "answer_id": "b",
            "answer": "How much you should weigh",
            "trivia_id": 10
        },
        {
            "answer_id": "c",
            "answer": "How many calories a food has",
            "trivia_id": 10
        },
        {
            "answer_id": "d",
            "answer": "How fast you digest food",
            "trivia_id": 10
        },

        {
            "answer_id": "a",
            "answer": "60 to 90",
            "trivia_id": 11
        },
        {
            "answer_id": "b",
            "answer": "80 to 130",
            "trivia_id": 11
        },
        {
            "answer_id": "c",
            "answer": "150 to 200",
            "trivia_id": 11
        },
        {
            "answer_id": "d",
            "answer": "30 to 70",
            "trivia_id": 11
        },

        {
            "answer_id": "a",
            "answer": "When your blood sugar is too high or too low",
            "trivia_id": 12
        },
        {
            "answer_id": "b",
            "answer": "When your heart rate is high",
            "trivia_id": 12
        },
        {
            "answer_id": "c",
            "answer": "When you eat too little",
            "trivia_id": 12
        },
        {
            "answer_id": "d",
            "answer": "When your weight increases",
            "trivia_id": 12
        },

        {
            "answer_id": "a",
            "answer": "Foods that turn into sugar in your body",
            "trivia_id": 13
        },
        {
            "answer_id": "b",
            "answer": "Foods that build muscles",
            "trivia_id": 13
        },
        {
            "answer_id": "c",
            "answer": "Types of protein",
            "trivia_id": 13
        },
        {
            "answer_id": "d",
            "answer": "Types of vitamins",
            "trivia_id": 13
        },

        {
            "answer_id": "a",
            "answer": "Shaky or dizzy",
            "trivia_id": 14
        },
        {
            "answer_id": "b",
            "answer": "Energetic",
            "trivia_id": 14
        },
        {
            "answer_id": "c",
            "answer": "Very full",
            "trivia_id": 14
        },
        {
            "answer_id": "d",
            "answer": "No appetite",
            "trivia_id": 14
        },

        {
            "answer_id": "a",
            "answer": "Very thirsty or tired",
            "trivia_id": 15
        },
        {
            "answer_id": "b",
            "answer": "Cold and shivering",
            "trivia_id": 15
        },
        {
            "answer_id": "c",
            "answer": "Hungry all the time",
            "trivia_id": 15
        },
        {
            "answer_id": "d",
            "answer": "Happy and energetic",
            "trivia_id": 15
        },

        {
            "answer_id": "a",
            "answer": "Checking your heart rate",
            "trivia_id": 16
        },
        {
            "answer_id": "b",
            "answer": "Testing your blood sugar",
            "trivia_id": 16
        },
        {
            "answer_id": "c",
            "answer": "Measuring temperature",
            "trivia_id": 16
        },
        {
            "answer_id": "d",
            "answer": "Taking medicine",
            "trivia_id": 16
        }
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