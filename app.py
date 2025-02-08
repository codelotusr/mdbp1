from flask import Flask
from flask_cors import CORS

from routes.people import people_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(people_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
