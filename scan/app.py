from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from scan import controllers

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')