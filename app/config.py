from datetime import timedelta


class Config:
    SERVER_NAME = None
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=365)

    APP_TITLE = "Just Color"
    APP_DESCRIPTION = "Just the color, and nothing else"
    APP_DOMAIN = "localhost:5000"
    APP_FAVICON_COLOR = "#000000"
    APP_FAVICON_WIDTH = 16
    APP_FAVICON_HEIGHT = 16
    APP_IMAGE_COLOR = "#000000"
    APP_IMAGE_WIDTH = 1200
    APP_IMAGE_HEIGHT = 630


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    SERVER_NAME = "justcolor.io"

    APP_DOMAIN = "justcolor.io"
