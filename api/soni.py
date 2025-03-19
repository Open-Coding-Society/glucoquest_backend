from flask import Flask, jsonify
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/data')
def get_data():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Soni",
        "LastName": "Dhenuva",
        "DOB": "January 29, 2009",
        "Residence": "San Diego",
        "Email": "sonika.dhenuva@gmail.com",
        "fav_booksAndMovies": ["Percy Jackson", "the Cruel Prince", "The Naturals", "Marvel", "Transformers", "Deadpool"]
    })

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Manasvi",
        "LastName": "Dhenuva",
        "DOB": "July 19, 2015",
        "Residence": "San Diego",
        "Email": "manasvi.dhenuva@gmail.com",
        "fav_books": ["Keeper of the Lost Cities", "Land of Stories", "Tales of Magic"]
    })
    
    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)