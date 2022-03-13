from flask import Flask
from flask import url_for

import os


def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "this-is-a-secret-key"

    # Register blueprints
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    # Cache related config
    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["q"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    return app
