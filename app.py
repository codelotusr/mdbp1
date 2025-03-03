from flask import Flask
from flask_cors import CORS

from routes.awards import awards_bp
from routes.genres import genres_bp
from routes.movies import movies_bp
from routes.people import people_bp
from routes.studios import studios_bp

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

app.register_blueprint(people_bp)
app.register_blueprint(genres_bp)
app.register_blueprint(studios_bp)
app.register_blueprint(movies_bp)
app.register_blueprint(awards_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
