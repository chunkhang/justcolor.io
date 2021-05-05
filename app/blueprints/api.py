import io

from flask import Blueprint, send_file
import png
from webcolors import hex_to_rgb

bp = Blueprint("api", __name__, url_prefix="/api")


PNG_DIMENSION_LIMIT = 2000


# Return PNG image with single color in provided dimensions
# Color should be in hex format: #000000
@bp.route("/png/<color>/<int:width>x<int:height>")
def png_api(color: str, width: int, height: int):
    if width > PNG_DIMENSION_LIMIT or height > PNG_DIMENSION_LIMIT:
        return "Dimension too large", 400

    try:
        rgb = tuple(hex_to_rgb(color))
    except ValueError:
        return "Invalid color", 400

    rows = []
    for row in range(height):
        row = []
        for col in range(width):
            row.extend(rgb)
        rows.append(tuple(row))

    buffer = io.BytesIO()
    writer = png.Writer(width, height, greyscale=False)
    writer.write(buffer, rows)
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")
