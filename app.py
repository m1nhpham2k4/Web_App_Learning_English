import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response
from datetime import timedelta


from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['CORS_HEADERS'] = 'Content-Type'

# username = os.environ["USERNAME"]
# password = os.environ["PASSWORD"]
# db_name = os.environ["DB_NAME"]
# host = os.environ["HOST"]
# port = os.environ["PORT"]
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
# local config database
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = f"postgresql://postgres.typysflflogppuumdsic:{password}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'test.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, use_reloader=False)
