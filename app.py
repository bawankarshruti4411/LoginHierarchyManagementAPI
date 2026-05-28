from flask import Flask
from flask_cors import CORS

from routes.auth import auth_bp
from routes.masters import masters_bp
from routes.operations import operations_bp
from routes.users import users_bp
from routes.permissions import permissions_bp

app = Flask(__name__)

# SECRET KEY
app.config["SECRET_KEY"] = "supersecretkey"

# ENABLE CORS
CORS(app)

# REGISTER ROUTES
app.register_blueprint(auth_bp)
app.register_blueprint(masters_bp)
app.register_blueprint(operations_bp)
app.register_blueprint(users_bp)
app.register_blueprint(permissions_bp)

# HEALTH CHECK ROUTE
@app.route("/")
def home():

    return {
        "status": "OK",
        "message": "Hierarchy Management API Running"
    }

# OPTIONAL EXTRA HEALTH ROUTE
@app.route("/health")
def health():

    return {
        "status": "healthy"
    }

# RUN SERVER
if __name__ == "__main__":

    app.run(debug=True)
