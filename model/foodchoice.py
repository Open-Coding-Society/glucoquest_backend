from flask_restful import Api, Resource
from sqlalchemy import Text, JSON
from __init__ import app, db
from sqlalchemy import Column, Integer, String, Text
from sqlite3 import IntegrityError

class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(Integer, primary_key=True)
    number = db.Column(Integer)
    food = db.Column(String, nullable=False)
    glycemic_index = db.Column(Integer, nullable=False)
    image = db.Column(String)

    def __repr__(self):
        return f"<Food(id={self.id}, number={self.number}, food={self.food}, glycemic_index={self.glycemic_index})>"

    # CRUD methods for Food class
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
            'number': self.number,
            'food': self.food,
            'glycemic_index': self.glycemic_index,
            'image': self.image,
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self
        
        number = inputs.get("number", None)
        food = inputs.get("food", None)
        glycemic_index = inputs.get("glycemic_index", None)
        image = inputs.get("image", None)

        if number:
            self.number = number
        if food:
            self.food = food
        if glycemic_index:
            self.glycemic_index = glycemic_index
        if image:
            self.image = image

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
        restored_foods = {}

        for food_data in data:  
            food_data.pop('id', None)

            # Check if the food already exists
            existing_food = Food.query.filter_by(
                food=food_data.get('food'),
                glycemic_index=food_data.get('glycemic_index')
            ).first()

            if existing_food:
                # Update the existing food with new data
                for key, value in food_data.items():
                    setattr(existing_food, key, value)

                try:
                    db.session.commit()
                    restored_foods[existing_food.id] = {
                        'status': 'updated',
                        'food': existing_food.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_foods[existing_food.id] = {
                        'status': 'error',
                        'message': str(e)
                    }
            else:
                # Create a new book
                new_food = Food(**food_data)
                db.session.add(new_food)
                try:
                    db.session.commit()
                    restored_foods[new_food.id] = {
                        'status': 'created',
                        'food': new_food.read()
                    }
                except Exception as e:
                    db.session.rollback()
                    restored_foods[new_food.id] = {
                        'status': 'error',
                        'message': str(e)
                    }

        return restored_foods
'''
        {
            "number": 1,
            "food": "",
            "glycemic_index": 1,
            "image": "{{site.baseurl}}/",
        },
 '''

def initFoods(): 
    food_data = [
        {
            "number": 1,
            "food": "Apple",
            "glycemic_index": 41,
            "image": "apple.png",
        },
        {
            "number": 1,
            "food": "Banana",
            "glycemic_index": 62,
            "image": "banana.png",
        },
        {
            "number": 2,
            "food": "Waffles",
            "glycemic_index": 77,
            "image": "waffle.png",
        },
        {
            "number": 2,
            "food": "Oatmeal",
            "glycemic_index": 53,
            "image": "oatmeal.png",
        },
        {
            "number": 3,
            "food": "Yogurt",
            "glycemic_index": 32,
            "image": "yogurt.png",
        },
        {
            "number": 3,
            "food": "Popcorn",
            "glycemic_index": 62,
            "image": "popcorn.png",
        },
        {
            "number": 4,
            "food": "Steamed white rice",
            "glycemic_index": 70,
            "image": "whiterice.png",
        },
        {
            "number": 4,
            "food": "Salmon",
            "glycemic_index": 0,
            "image": "salmon.png",
        },
    ]       
    
  
    for food in food_data:
        if not Food.query.filter_by(food=food["food"]).first():  # check if food already exists aviods duplicates
            new_food = Food(
                number=food["number"],
                food=food["food"],
                glycemic_index=food["glycemic_index"],
                image=food["image"]
            )
            db.session.add(new_food) 
    
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
    initFoods()