# Required to allow reading of jpegData. Flask must be imported after this code.
import formparser_override

# Now we can continue.
import colorama
import sentry_sdk
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration

from debug import request_dump

from werkzeug import exceptions
from flask import Flask, request

# Import crucial components
import config

if config.use_sentry:
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        integrations=[FlaskIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
import models

# Create schema and migrate accordingly
migrate = Migrate(app, db, compare_type=True)
with app.test_request_context():
    db.init_app(app)
    db.create_all()

# Enable debug printing
debug = app.debug
if debug:
    colorama.init()

# These require database access.
from camlib import response
from routes import action_list, file_action_list
import render


@app.route("/wii_svr/WPOperationServlet", methods=["GET", "POST"])
def op_servlet():
    if debug:
        request_dump(request)

    try:
        action = request.headers["Operation"]
        return action_list[action](request)
    except KeyError:
        # This is not an action or a format we know of.
        return exceptions.NotFound()


@app.route("/wii_svr/WPFileOperationServlet", methods=["GET", "POST"])
@response()
def file_op_servlet():
    if debug:
        request_dump(request)

    try:
        action = request.headers["Operation"]
        return file_action_list[action](request)
    except KeyError:
        return exceptions.NotFound()
