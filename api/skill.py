from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.skill import Skill  # Import the Skill model

# Create a Blueprint for the skill API
skill_api = Blueprint('skill_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(skill_api)

class SkillAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new skill."""
            data = request.get_json()
            if not data or 'user_id' not in data or 'skill_name' not in data or 'expertise_level' not in data:
                return {"message": "Missing required fields"}, 400

            try:
                # Create a Skill instance
                skill = Skill(
                    user_id=data['user_id'],
                    skill_name=data['skill_name'],
                    expertise_level=data['expertise_level']
                )
                skill.create()
                return jsonify(skill.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific skill by ID."""
            data = request.get_json()
            if not data or 'skill_id' not in data:
                return {"message": "Skill ID required"}, 400

            skill = Skill.query.get(data['skill_id'])
            if not skill:
                return {"message": "Skill not found"}, 404

            return jsonify(skill.read())

        @token_required()
        def put(self):
            """Update an existing skill."""
            data = request.get_json()
            if not data or 'skill_id' not in data:
                return {"message": "Skill ID required"}, 400

            skill = Skill.query.get(data['skill_id'])
            if not skill:
                return {"message": "Skill not found"}, 404

            try:
                skill.skill_name = data.get('skill_name', skill.skill_name)
                skill.expertise_level = data.get('expertise_level', skill.expertise_level)
                skill.create()
                return jsonify(skill.read())
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all skills."""
            skills = Skill.query.all()
            return jsonify([skill.read() for skill in skills])

# Map API endpoints
api.add_resource(SkillAPI._CRUD, '/skill')
api.add_resource(SkillAPI._ALL, '/skill/all')

#TESTING IN POSTMAN
#Authenticate --> {"uid": "toby", "password": "123Toby!"} 
#GET data --> { "skill_id": 1 }
#PUT updates skill --> {  "skill_id": 1, "skill_name": "Updated Skill Name",  "expertise_level": "Updated Expertise Level"}
#POST add data ---> {"user_id": 1, "skill_name": "Python Development",  "expertise_level": "Advanced"}
# ./scripts/db_init.py 
# ./scripts/db_backup.py
# ./scripts/db_restore.py