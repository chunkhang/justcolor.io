import os

from app.main import create_app
from app.config import DevelopmentConfig, ProductionConfig

environment = os.environ.get("FLASK_ENV", "production")
cfg = DevelopmentConfig if environment == "development" else ProductionConfig

app = create_app(cfg)
