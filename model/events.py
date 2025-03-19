# imports from flask
import logging
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import app, db  # Assuming __init__.py initializes app and db
from datetime import datetime
from flask import request
from model.user import User  # Import the User model

# Event Model
class Event(db.Model):
    __tablename__ = 'events'

    # Define user_id as the first column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # New user_id column
    event_id = db.Column(db.Integer, primary_key=True)  # Primary key for the event
    name = db.Column(db.String(255), nullable=False)  # Event name
    location = db.Column(db.String(255), nullable=False)  # Event location
    date = db.Column(db.Date, nullable=False)  # Event date (without time)

    def __init__(self, name, location, date, user_id):
        self.name = name
        self.location = location
        self.date = date
        self.user_id = user_id  # Store the user_id

    def __repr__(self):
        return f"Event(id={self.event_id}, name={self.name}, location={self.location}, date={self.date}, user_id={self.user_id})"

    def create(self):
        """Creates a new event in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error creating event '{self.name}': {str(e)}")
            return None
        return self

    def read(self):
        """Returns a dictionary representation of the event."""
        return {
            "event_id": self.event_id,
            "name": self.name,
            "location": self.location,
            "date": self.date.isoformat(),
            "user_id": self.user_id  # Include the user_id in the read data
        }

    def update(self, data):
        """Updates the event with new data."""
        self.name = data.get('name', self.name)
        self.location = data.get('location', self.location)
        if 'date' in data:
            try:
                self.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return None  # Invalid date format
        if 'user_id' in data:
            self.user_id = data.get('user_id', self.user_id)  # Update user_id if provided

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error updating event '{self.name}': {str(e)}")
            return None
        return self

    def delete(self):
        """Deletes the event from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error deleting event '{self.name}': {str(e)}")
            return None
        return self


# Initialize sample events
def initEvents():
    """Initialize some sample events in the database."""
    events = [
        Event(name='Tech Conference 2025', location='San Francisco Convention Center, San Francisco, CA', date=datetime(2025, 3, 12).date(), user_id=1),
        Event(name='Cooking Masterclass', location='Culinary Institute of America, Napa Valley, CA', date=datetime(2025, 4, 5).date(), user_id=2),
        Event(name='AI and Machine Learning Workshop', location='MIT Media Lab, Cambridge, MA', date=datetime(2025, 6, 10).date(), user_id=3),
        Event(name='Music Festival 2025', location='Central Park, New York City, NY', date=datetime(2025, 7, 1).date(), user_id=1)
    ]

    for event in events:
        try:
            db.session.add(event)
            db.session.commit()
            print(f"Event created: {event.name}")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Failed to create event: {event.name}. Error: {str(e)}")


# API routes to interact with events
@app.route('/events', methods=['GET'])
def get_events():
    """Returns a list of all events."""
    events = Event.query.all()
    return jsonify([event.read() for event in events])


@app.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Returns a specific event by its ID."""
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.read())
    return jsonify({'error': 'Event not found'}), 404


@app.route('/event', methods=['POST'])
def create_event():
    """Creates a new event."""
    data = request.get_json()
    try:
        event_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    event = Event(
        name=data.get('name'),
        location=data.get('location'),
        date=event_date,
        user_id=data.get('user_id')  # Make sure the user_id is passed in the request
    )
    event.create()
    return jsonify(event.read()), 201


@app.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Updates an existing event."""
    event = Event.query.get(event_id)
    if event:
        data = request.get_json()
        if event.update(data) is None:
            return jsonify({'error': 'Invalid data provided for update.'}), 400
        return jsonify(event.read())
    return jsonify({'error': 'Event not found'}), 404


@app.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Deletes an event."""
    event = Event.query.get(event_id)
    if event:
        event.delete()
        return jsonify({'message': 'Event deleted successfully'}), 200
    return jsonify({'error': 'Event not found'}), 404


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
