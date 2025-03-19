from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import db
from model.user import User  # Import User model for foreign key reference

app = Flask(__name__)

# Survey Model (Already defined, for reference)
class Survey(db.Model):
    __tablename__ = 'surveys'  # Plural table name for consistency

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id

    def __repr__(self):
        return f"Survey(id={self.id}, message={self.message}, user_id={self.user_id})"

    def create(self):
        """Adds a new survey response to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError("Survey response creation failed due to a database error.")

    def read(self):
        """Returns a dictionary representation of the survey response."""
        return {
            'id': self.id,
            'message': self.message,
            'user_id': self.user_id
        }

    def delete(self):
        """Deletes the survey response from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError("Survey response deletion failed due to a database error.")

# Initialize your app (you may already have this code elsewhere)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # or any other database URI
db.init_app(app)

# Survey API Endpoint
@app.route('/api/survey', methods=['POST'])
def add_survey():
    """Endpoint to create a new survey response."""
    try:
        # Get the data from the incoming request
        data = request.get_json()

        # Check if required data is provided
        if 'message' not in data or 'user_id' not in data:
            return jsonify({"error": "Both 'message' and 'user_id' are required."}), 400

        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Create new Survey instance and save it
        new_survey = Survey(message=data['message'], user_id=data['user_id'])
        new_survey.create()  # Commit to the database

        # Return success response with the newly created survey data
        return jsonify(new_survey.read()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Sample function to initialize sample surveys (optional)
def init_surveys():
    """Initialize some sample survey responses in the database."""
    user = User.query.first()  # Ensure a user exists before creating sample data
    if user:
        sample_survey = Survey(message="Great experience!", user_id=user.id)
        try:
            sample_survey.create()
            print("Survey sample data initialized.")
        except IntegrityError as e:
            print(f"Error initializing survey data: {e}")
    else:
        print("No users found. Please create a user before initializing surveys.")



# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8209)