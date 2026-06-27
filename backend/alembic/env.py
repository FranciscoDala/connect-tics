import sys, os
from dotenv import load_dotenv
load_dotenv()

# GAMBIARRA QUE FUNCIONA 100%: Adiciona a pasta BACKEND no PYTHONPATH
# Porque o 'src' está dentro de backend
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

from src.database.models import Base 

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
target_metadata = Base.metadata
# ...resto do arquivo igual