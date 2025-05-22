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
    glycemic_load = db.Column(Integer, nullable=False)
    info = db.Column(String, nullable=False)
    image = db.Column(String)

    def __repr__(self):
        return f"<Food(id={self.id}, number={self.number}, food={self.food}, glycemic_load={self.glycemic_load}, info={self.info})>"

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
            'glycemic_load': self.glycemic_load,
            'info': self.info,
            'image': self.image,
        }

    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self
        
        number = inputs.get("number", None)
        food = inputs.get("food", None)
        glycemic_load = inputs.get("glycemic_load", None)
        info = inputs.get("info", None)
        image = inputs.get("image", None)

        if number:
            self.number = number
        if food:
            self.food = food
        if glycemic_load:
            self.glycemic_load = glycemic_load
        if info:
            self.info = info
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
                glycemic_load=food_data.get('glycemic_load')
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
                # Create a new food
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

def initFoods(): 
    food_data = [
        {
            "number": 1,
            "food": "Apple",
            "glycemic_load": 5,
            "info": "A delicious and low-carb snack",
            "image": "apple.png",
        },
        {
            "number": 1,
            "food": "Banana",
            "glycemic_load": 10.1,
            "info": "Good for increasing blood glucose when needed, but to be eaten with care",
            "image": "banana.png",
        },
        {
            "number": 2,
            "food": "Waffles",
            "glycemic_load": 54.3,
            "info": "A carb-heavy start to the day can trigger high blood glucose in the morning",
            "image": "waffles.png",
        },
        {
            "number": 2,
            "food": "Oatmeal",
            "glycemic_load": 9,
            "info": "A classic, customizable choice with less carbohydrates",
            "image": "oatmeal.png",
        },
        {
            "number": 3,
            "food": "Yogurt",
            "glycemic_load": 1.3,
            "info": "A refreshing snack to get through the day",
            "image": "yogurt.png",
        },
        {
            "number": 3,
            "food": "Popcorn",
            "glycemic_load": 40.7,
            "info": "Fine for special occasions, but to be eaten sparingly",
            "image": "popcorn.png",
        },
        {
            "number": 4,
            "food": "Steamed white rice",
            "glycemic_load": 56,
            "info": "Classic dinner component with hidden carbohydrates which can cause late-night glucose spikes",
            "image": "whiterice.png",
        },
        {
            "number": 4,
            "food": "Salmon",
            "glycemic_load": 0,
            "info": "As a protien, salmon has no carbohydrates and a glycemic load of 0!",
            "image": "salmon.png",
        },
        {
            "number": 5,
            "food": "Chocolate",
            "glycemic_load": 29.9,
            "info": "Note the difference in glycemic load between the chocolates",
            "image": "chocolate.png",
        },
        {
            "number": 5,
            "food": "Dark chocolate",
            "glycemic_load": 13.8,
            "info": "Sometimes a food can still be diabetes-friendly with minor adjustments",
            "image": "darkchocolate.png",
        },
        {
            "number": 6,
            "food": "Milk",
            "glycemic_load": 1.6,
            "info": "Perfect breakfast companion",
            "image": "milk.png",
        },
        {
            "number": 6,
            "food": "Soda",
            "glycemic_load": 6.0,
            "info": "To be drank mindfully",
            "image": "soda.png",
        },
        {
            "number": 7,
            "food": "Chicken",
            "glycemic_load": 0,
            "info": "Sometimes, multiple options can be good for blood glucose levels",
            "image": "chicken.png",
        },
        {
            "number": 7,
            "food": "Beef",
            "glycemic_load": 0,
            "info": "Sometimes, multiple options can be good for blood glucose levels",
            "image": "beef.png",
        },
        {
            "number": 8,
            "food": "Boiled potato",
            "glycemic_load": 12.3,
            "info": "Notice how preparing the same food differently can vastly change its available carbs and glycemic load",
            "image": "boiledpotato.png",
        },
        {
            "number": 8,
            "food": "Fried potato",
            "glycemic_load": 19.1,
            "info": "Notice how preparing the same food differently can vastly change its available carbs and glycemic load",
            "image": "friedpotato.png",
        },
        {
            "number": 9,
            "food": "White bread",
            "glycemic_load": 39.4,
            "info": "Typical sandwich ingredient",
            "image": "whitebread.png",
        },
        {
            "number": 9,
            "food": "Lettuce",
            "glycemic_load": 0.5,
            "info": "Low-carb alternative to bread, which can be used to make lettuce wraps or other meals",
            "image": "lettuce.png",
        },
        {
            "number": 10,
            "food": "Spaghetti",
            "glycemic_load": 12.8,
            "info": "Comfort food for many",
            "image": "spaghetti.png",
        },
        {
            "number": 10,
            "food": "Pizza",
            "glycemic_load": 19.8,
            "info": "Comfort food for many",
            "image": "pizza.png",
        },
    ]       
    
  
    for food in food_data:
        if not Food.query.filter_by(food=food["food"]).first():  # check if food already exists aviods duplicates
            new_food = Food(
                number=food["number"],
                food=food["food"],
                glycemic_load=food["glycemic_load"],
                info=food["info"],
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