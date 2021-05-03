from base64 import b64encode
import io
import os
import re

from flask import Flask, render_template, redirect, url_for
from webcolors import normalize_hex, name_to_hex, hex_to_rgb
import png

app = Flask(__name__)

APP_NAME = "Just Color"
APP_SLOGAN = "Just the color, and nothing else"
APP_BASE_URL = "justcolor.io"
APP_FAVICON_COLOR = "#000"
ICON_SIZE = 32
HEX_PATTERN = r"^([0-9a-fA-F]{3}){1,2}$"
NAME_PATTERN = r"^[a-zA-Z]{1,20}$"


# Return Base64-encoded PNG for a simple color square
# Pass in color in hex format
def generate_icon(color: str) -> str:
    rgb = tuple(hex_to_rgb(color))

    rows = []
    for row in range(ICON_SIZE):
        row = []
        for col in range(ICON_SIZE):
            row.extend(rgb)
        rows.append(tuple(row))

    buffer = io.BytesIO()
    writer = png.Writer(width=ICON_SIZE, height=ICON_SIZE, greyscale=False)
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
    template_globals = {
        "APP_NAME": APP_NAME,
        "APP_SLOGAN": APP_SLOGAN,
        "APP_BASE_URL": APP_BASE_URL,
        "APP_FAVICON": generate_icon(APP_FAVICON_COLOR),
    }

    return dict(**template_globals)


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
    if re.search(HEX_PATTERN, query):
        color = normalize_hex(f"#{query}")
    # Name (black)
    if re.search(NAME_PATTERN, query):
        try:
            color = name_to_hex(query)
        except ValueError:
            pass

    if not color:
        return render_template("pages/color_not_found.html")

    return render_template("pages/color.html", color=color, icon=generate_icon(color))


@app.errorhandler(404)
def not_found_page(error):
    return redirect(url_for("home_page"))
