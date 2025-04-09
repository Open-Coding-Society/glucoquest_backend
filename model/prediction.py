# imports from flask
import logging
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from __init__ import app, db  # Assuming __init__.py initializes app and db
from datetime import datetime
from model.user import User  # Import the User model

# DiabetesPrediction Model
class DiabetesPrediction(db.Model):
    __tablename__ = 'diabetes_predictions'

    # Define user_id as a foreign key referencing the 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # user_id foreign key
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the prediction
    probability = db.Column(db.Float, nullable=False)  # Probability of diabetes
    risk_level = db.Column(db.String(20), nullable=False)  # Risk level (e.g., Low, Medium, High)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of the prediction

    # Define relationship to User model
    user = db.relationship('User', backref=db.backref('diabetes_predictions', lazy=True))

    def __init__(self, user_id, probability, risk_level):
        self.user_id = user_id
        self.probability = probability
        self.risk_level = risk_level

    def __repr__(self):
        return f"<DiabetesPrediction(id={self.id}, user_id={self.user_id}, probability={self.probability}, risk_level={self.risk_level})>"

    def create(self):
        """Creates a new prediction in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error creating prediction for user '{self.user_id}': {str(e)}")
            return None
        return self

    def read(self):
        """Returns a dictionary representation of the prediction."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "probability": self.probability,
            "risk_level": self.risk_level,
            "timestamp": self.timestamp.isoformat()  # Format timestamp as ISO
        }

    def update(self, data):
        """Updates the prediction with new data."""
        self.probability = data.get('probability', self.probability)
        self.risk_level = data.get('risk_level', self.risk_level)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error updating prediction for user '{self.user_id}': {str(e)}")
            return None
        return self

    def delete(self):
        """Deletes the prediction from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error deleting prediction for user '{self.user_id}': {str(e)}")
            return None
        return self

# API routes to interact with diabetes predictions
@app.route('/diabetes_predictions', methods=['GET'])
def get_predictions():
    """Returns a list of all diabetes predictions."""
    predictions = DiabetesPrediction.query.all()
    return jsonify([prediction.read() for prediction in predictions])

@app.route('/diabetes_prediction/<int:id>', methods=['GET'])
def get_prediction(id):
    """Returns a specific diabetes prediction by its ID."""
    prediction = DiabetesPrediction.query.get(id)
    if prediction:
        return jsonify(prediction.read())
    return jsonify({'error': 'Prediction not found'}), 404

@app.route('/diabetes_prediction', methods=['POST'])
def create_prediction():
    """Creates a new diabetes prediction."""
    data = request.get_json()
    
    # Ensure necessary fields are present
    if 'user_id' not in data or 'probability' not in data or 'risk_level' not in data:
        return jsonify({'error': 'Missing required fields: user_id, probability, risk_level'}), 400

    prediction = DiabetesPrediction(
        user_id=data.get('user_id'),
        probability=data.get('probability'),
        risk_level=data.get('risk_level')
    )
    prediction.create()
    return jsonify(prediction.read()), 201

@app.route('/diabetes_prediction/<int:id>', methods=['PUT'])
def update_prediction(id):
    """Updates an existing diabetes prediction."""
    prediction = DiabetesPrediction.query.get(id)
    if prediction:
        data = request.get_json()
        if prediction.update(data) is None:
            return jsonify({'error': 'Invalid data provided for update.'}), 400
        return jsonify(prediction.read())
    return jsonify({'error': 'Prediction not found'}), 404

@app.route('/diabetes_prediction/<int:id>', methods=['DELETE'])
def delete_prediction(id):
    """Deletes a diabetes prediction."""
    prediction = DiabetesPrediction.query.get(id)
    if prediction:
        prediction.delete()
        return jsonify({'message': 'Prediction deleted successfully'}), 200
    return jsonify({'error': 'Prediction not found'}), 404

# Initialize sample predictions (if needed)
def initPredictions():
    """Initialize some sample predictions in the database."""
    predictions = [
        DiabetesPrediction(user_id=1, probability=0.65, risk_level="Medium"),
        DiabetesPrediction(user_id=2, probability=0.82, risk_level="High")
    ]

    for prediction in predictions:
        try:
            db.session.add(prediction)
            db.session.commit()
            print(f"Prediction created for user '{prediction.user_id}'")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Failed to create prediction for user '{prediction.user_id}'. Error: {str(e)}")

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
