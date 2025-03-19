import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.events import Event  # Import the Event model

# Create a Blueprint for the event API
event_api = Blueprint('event_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(event_api)

class EventAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new event."""
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data:
                return {'message': 'Event name is required'}, 400
            if 'location' not in data:
                return {'message': 'Event location is required'}, 400
            if 'date' not in data:
                return {'message': 'Event date is required'}, 400

            # Validate the date format (YYYY-MM-DD)
            try:
                event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

            # Create an Event instance
            event = Event(
                name=data['name'],
                location=data['location'],
                date=event_date,
                user_id=current_user.id  # Attach the current user ID to the event
            )

            # Save the event object using the ORM method defined in the model
            event.create()
            return jsonify(event.read())

        @token_required()
        def get(self):
            """Retrieve a specific event by ID."""
            data = request.get_json()
            if not data or 'event_id' not in data:
                return {"message": "Event ID required"}, 400

            event = Event.query.get(data['event_id'])
            if not event:
                return {"message": "Event not found"}, 404

            return jsonify(event.read())

        @token_required()
        def put(self):
            """Update an existing event."""
            data = request.get_json()
            if not data or 'event_id' not in data:
                return {"message": "Event ID required"}, 400

            event = Event.query.get(data['event_id'])
            if not event:
                return {"message": "Event not found"}, 404

            try:
                if 'name' in data:
                    event.name = data['name']
                if 'location' in data:
                    event.location = data['location']
                if 'date' in data:
                    try:
                        event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                    except ValueError:
                        return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

                event.update()
                return jsonify(event.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete an event."""
            data = request.get_json()
            if not data or 'event_id' not in data:
                return {"message": "Event ID required"}, 400

            event = Event.query.get(data['event_id'])
            if not event:
                return {"message": "Event not found"}, 404

            try:
                event.delete()
                return {"message": "Event deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all events."""
            events = Event.query.all()
            return jsonify([event.read() for event in events])

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Retrieve events by user ID."""
            events = Event.query.filter_by(user_id=user_id).all()  # Filter events by user_id
            if not events:
                return {"message": "No events found for this user."}, 404
            return jsonify([event.read() for event in events])

# Map API endpoints
api.add_resource(EventAPI._CRUD, '/event')
api.add_resource(EventAPI._ALL, '/events')
api.add_resource(EventAPI._BY_USER, '/events/user/<int:user_id>')  # New endpoint to get events by user ID
