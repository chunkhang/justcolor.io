import re

from flask import Blueprint, render_template
from webcolors import name_to_hex, normalize_hex

bp = Blueprint("page", __name__)


@bp.route("/")
def home_page():
    return render_template("pages/home.html")


@bp.route("/robots.txt")
def robots_page():
    return bp.send_static_file("robots.txt")


COLOR_HEX_PATTERN = r"^([0-9a-fA-F]{3}){1,2}$"
COLOR_NAME_PATTERN = r"^[a-zA-Z]{1,20}$"


@bp.route("/<string:query>")
def color_page(query):
    color = None

    # Hex (000, 000000)
    if re.search(COLOR_HEX_PATTERN, query):
        color = normalize_hex(f"#{query}")
    # Name (black)
    if re.search(COLOR_NAME_PATTERN, query):
        try:
            color = name_to_hex(query)
        except ValueError:
            pass

    if not color:
        return render_template("pages/color_not_found.html")

    return render_template("pages/color.html", color=color)
