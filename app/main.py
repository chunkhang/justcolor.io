import io
import os
import re
from base64 import b64encode
from typing import Type

from flask import Flask, redirect, render_template, url_for
from flask_minify import minify
import png
from webcolors import hex_to_rgb, name_to_hex, normalize_hex

from app.config import Config


def create_app(cfg: Type[Config]):
    app = Flask(__name__)
    app.config.from_object(cfg)
    minify(app=app, html=True, js=True, cssless=True)

    # Return Base64-encoded PNG for a simple color square
    # Pass in color in hex format
    def generate_icon(color: str) -> str:
        rgb = tuple(hex_to_rgb(color))

        size = app.config["ICON_SIZE"]

        rows = []
        for row in range(size):
            row = []
            for col in range(size):
                row.extend(rgb)
            rows.append(tuple(row))

        buffer = io.BytesIO()
        writer = png.Writer(width=size, height=size, greyscale=False)
        writer.write(buffer, rows)

        icon = b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{icon}"

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
        return dict(
            **{
                **app.config,
                "APP_FAVICON": generate_icon(app.config["APP_FAVICON_COLOR"]),
            }
        )

    @app.route("/")
    def home_page():
        return render_template("pages/home.html")

    @app.route("/robots.txt")
    def robots_page():
        return app.send_static_file("robots.txt")

    @app.route("/<string:query>")
    def color_page(query):
        color = None

        # Hex (000, 000000)
        if re.search(app.config["COLOR_HEX_PATTERN"], query):
            color = normalize_hex(f"#{query}")
        # Name (black)
        if re.search(app.config["COLOR_NAME_PATTERN"], query):
            try:
                color = name_to_hex(query)
            except ValueError:
                pass

        if not color:
            return render_template("pages/color_not_found.html")

        return render_template(
            "pages/color.html", color=color, icon=generate_icon(color)
        )

    @app.errorhandler(404)
    def not_found_page(error):
        return redirect(url_for("home_page"))

    return app
