from datetime import datetime
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.notifications import Notification  # Import the Notification model
from model.user import User  # Import the User model to validate recipient

# Create a Blueprint for the notifications API
notifications_api = Blueprint('notifications_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(notifications_api)

class NotificationAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new notification."""
            data = request.get_json()
            if not data or 'content' not in data or 'recipient_id' not in data:
                return {"message": "Missing required fields"}, 400

            try:
                # Get the current user ID from the token
                sender_id = g.current_user.id  # Assuming current user ID is accessible from the JWT token

                # Check if the recipient exists
                recipient_id = data['recipient_id']
                recipient = User.query.filter_by(id=recipient_id).first()
                if not recipient:
                    return {"message": f"Recipient with ID {recipient_id} not found"}, 404

                # Create a Notification instance
                notification = Notification(
                    content=data['content'],
                    user_id=sender_id,  # The sender's ID
                    recipient_id=recipient_id  # The recipient's ID
                )
                notification.create()
                return jsonify(notification.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific notification by ID."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Notification ID required"}, 400

            notification = Notification.query.get(data['id'])
            if not notification:
                return {"message": "Notification not found"}, 404

            return jsonify(notification.read())

        @token_required()
        def delete(self):
            """Delete a notification."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Notification ID required"}, 400

            notification = Notification.query.get(data['id'])
            if not notification:
                return {"message": "Notification not found"}, 404

            try:
                notification.delete()
                return {"message": "Notification deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all notifications for the current user."""
            current_user_id = g.current_user.id  # Get the current user's ID from the token
            notifications = Notification.query.filter_by(recipient_id=current_user_id).all()
            return jsonify([notification.read() for notification in notifications])

# Map API endpoints
api.add_resource(NotificationAPI._CRUD, '/notification')
api.add_resource(NotificationAPI._ALL, '/notifications')
