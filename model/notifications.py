from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Sender's user ID
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Recipient's user ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Define relationships for easy access to sender and recipient
    user = db.relationship('User', foreign_keys=[user_id], backref='sent_notifications')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_notifications')

    def __init__(self, content, user_id, recipient_id):
        """
        Constructor for the Notification class.
        
        Args:
            content (str): The content of the notification.
            user_id (int): The ID of the user associated with the notification (sender).
            recipient_id (int): The ID of the user receiving the notification.
        """
        self.content = content
        self.user_id = user_id
        self.recipient_id = recipient_id

    def create(self):
        """
        Adds the notification to the database and commits the transaction.
        
        Raises:
            Exception: If there is an error during the database transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieves the notification data as a dictionary.
        
        Returns:
            dict: A dictionary containing the notification data.
        """
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'recipient_id': self.recipient_id,
            'created_at': self.created_at
        }

    @staticmethod
    def init_notifications():
        """
        Initializes sample notifications for the first user in the database.
        """
        user = User.query.first()
        if user:
            sample_notification = Notification(content='Welcome to our platform!', user_id=user.id, recipient_id=user.id)
            try:
                sample_notification.create()
                print("Sample notification created successfully.")
            except Exception as e:
                print(f"Error creating sample notification: {e}")
        else:
            print("No user found to create sample notifications.")
