from flask import Blueprint
from flask_restful import Api, Resource  # used for REST API building

# Create a Blueprint for the API
student_api = Blueprint('student_api', __name__, url_prefix='/api')

# Initialize the Flask-RESTful API
api = Api(student_api)

# Define the StudentAPI with its individual endpoints
class StudentAPI:
    class _Spencer(Resource):
        def get(self):
            spencer_data = {
                "FirstName": "Spencer",
                "LastName": "Lyons",
                "DOB": "September 11, 2001",
                "Residence": "San Diego",
                "Email": "spencerl11709@stu.powyusd.com",
                "age": "15"
            }
            return spencer_data
        
    class _Kushi(Resource):
        def get(self):
            kushi_data = {
                "FirstName": "Kushi",
                "LastName": "Gade",
                "DOB": "January 23, 2009",
                "Residence": "San Diego",
                "Email": "kushig507@gmail.com",
                "age": "15"
            }
            return kushi_data
        
    class _Nora(Resource):
        def get(self):
            nora_data = {
                "FirstName": "Nora",
                "LastName": "Ahadian",
                "DOB": "May 24, 2009",
                "Residence": "San Diego",
                "Email": "Nahadian@stu.powayusd.com",
                "age": "15"
            }
            return nora_data

    class _Soni(Resource):
        def get(self):
            soni_data = {
                "FirstName": "Soni",
                "LastName": "Dhenuva",
                "DOB": "January 29, 2009",
                "Residence": "San Diego",
                "Email": "sonika.dhenuva@gmail.com",
                "age": "15"
            }
            return soni_data

    class _Vibha(Resource):
        def get(self):
            vibha_data = {
                "FirstName": "Vibha",
                "LastName": "Mandayam",
                "DOB": "October 19, 2008",
                "Residence": "San Diego",
                "Email": "vibhamandayam08@gmail.com",
                "age": "16"
            }
            return vibha_data

    class _AllStudents(Resource):
        def get(self):
            # Consolidate all student data into a list
            all_students_data = [
                {
                    "FirstName": "Spencer",
                    "LastName": "Lyons",
                    "DOB": "September 11, 2001",
                    "Residence": "San Diego",
                    "Email": "spencerl11709@stu.powyusd.com",
                    "age": "15"
                },
                {
                    "FirstName": "Kushi",
                    "LastName": "Gade",
                    "DOB": "January 23, 2009",
                    "Residence": "San Diego",
                    "Email": "kushig507@gmail.com",
                    "age": "15"
                },
                {
                    "FirstName": "Nora",
                    "LastName": "Ahadian",
                    "DOB": "May 24, 2009",
                    "Residence": "San Diego",
                    "Email": "Nahadian@stu.powayusd.com",
                    "age": "15"
                },
                {
                    "FirstName": "Soni",
                    "LastName": "Dhenuva",
                    "DOB": "January 29, 2009",
                    "Residence": "San Diego",
                    "Email": "sonika.dhenuva@gmail.com",
                    "age": "15"
                },
                {
                    "FirstName": "Vibha",
                    "LastName": "Mandayam",
                    "DOB": "October 19, 2008",
                    "Residence": "San Diego",
                    "Email": "vibhamandayam08@gmail.com",
                    "age": "16"
                }
            ]
            return all_students_data

    # Building REST API endpoints
    api.add_resource(_Spencer, '/student/spencer')
    api.add_resource(_Kushi, '/student/kushi')
    api.add_resource(_Nora, '/student/nora')
    api.add_resource(_Soni, '/student/soni')
    api.add_resource(_Vibha, '/student/vibha')
    api.add_resource(_AllStudents, '/students/all')  # Add the bulk resource
