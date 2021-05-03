import os

from flask import Flask, render_template, redirect, url_for
from webcolors import normalize_hex, name_to_hex
import re

app = Flask(__name__)

HEX_PATTERN = r"^([0-9a-fA-F]{3}){1,2}$"
NAME_PATTERN = r"^[a-zA-Z]{1,20}$"


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
        "APP_NAME": "Just Color",
        "APP_SLOGAN": "Just the color, and nothing else",
        "APP_BASE_URL": "justcolor.io",
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
        except:
            pass

    if not color:
        return render_template("pages/color_not_found.html")

    return render_template("pages/color.html", color=color)


@app.errorhandler(404)
def not_found_page(error):
    return redirect(url_for("home_page"))
