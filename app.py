from flask import Flask, render_template
from markupsafe import escape
from webcolors import normalize_hex, name_to_hex
import re

app = Flask(__name__)

HEX_PATTERN = r'^([0-9a-fA-F]{3}){1,2}$'
NAME_PATTERN = r'^[a-zA-Z]{1,20}$'


@app.route('/')
def home_page():
    return 'Hello, World!'


@app.errorhandler(404)
def not_found_page(error):
    return render_template('not_found.html'), 404


@app.route('/<string:query>')
def color_page(query):
    color = None

    # Hex (000, 000000)
    if re.search(HEX_PATTERN, query):
        color = normalize_hex(f'#{query}')
    # Name (black)
    if re.search(NAME_PATTERN, query):
        try:
            color = name_to_hex(query)
        except:
            pass

    if not color:
        return render_template('error.html', query=escape(query))

    return render_template('color.html', color=color)