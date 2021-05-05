import os
from typing import Type

from flask import Flask, redirect, url_for
from flask_minify import minify

from app.blueprints import api, page
from app.config import Config


def create_app(cfg: Type[Config]):
    app = Flask(__name__)
    app.config.from_object(cfg)
    minify(app=app, html=True, js=True, cssless=True)

    app.register_blueprint(api.bp)
    app.register_blueprint(page.bp)

    # Fix caching for static files
    # https://gist.github.com/itsnauman/b3d386e4cecf97d59c94
    @app.context_processor
    def override_url_for():
        def dated_url_for(endpoint, **values):
            if endpoint == "static":
                filename = values.get("filename", None)
                if filename:
                    file_path = os.path.join(app.root_path, endpoint, filename)
                    values["q"] = int(os.stat(file_path).st_mtime)
            return url_for(endpoint, **values)

        return dict(url_for=dated_url_for)

    # Inject global variables in templates
    # https://stackoverflow.com/questions/43335931/global-variables-in-flask-templates
    @app.context_processor
    def inject_template_globals():
        return dict(**app.config)

    # Redirect to home page when route not found
    @app.errorhandler(404)
    def not_found(error):
        return redirect(url_for("page.home_page"))

    return app
