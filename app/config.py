from datetime import timedelta


class Config:
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=365)

    APP_NAME = "Just Color"
    APP_SLOGAN = "Just the color, and nothing else"
    APP_BASE_URL = "http://localhost:5000"
    APP_FAVICON_COLOR = "#000"
    ICON_SIZE = 32

    COLOR_HEX_PATTERN = r"^([0-9a-fA-F]{3}){1,2}$"
    COLOR_NAME_PATTERN = r"^[a-zA-Z]{1,20}$"


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    APP_BASE_URL = "https://justcolor.io"
