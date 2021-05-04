import os

from app.config import DevelopmentConfig, ProductionConfig
from app.main import create_app

environment = os.environ.get("FLASK_ENV", "production")
cfg = DevelopmentConfig if environment == "development" else ProductionConfig

app = create_app(cfg)
