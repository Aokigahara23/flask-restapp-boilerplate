from os import getenv

from src.app import create_app
from src.config import DevConfig, ProdConfig

app = create_app(ProdConfig if getenv('VDASHBOARD_PROD_ENV') else DevConfig)
