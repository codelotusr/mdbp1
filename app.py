from flask import Flask
from flask_cors import CORS

from routes.genres import genres_bp
from routes.people import people_bp

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

app.register_blueprint(people_bp)
app.register_blueprint(genres_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
