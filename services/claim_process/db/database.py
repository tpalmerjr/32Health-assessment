import os
from sqlmodel import SQLModel, create_engine

from . import models

POSTGRES_DB = os.environ.get('POSTGRES_DB', 'backenddb')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'backenduser')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'backendsecretpassword')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

# SQL connection url string
sql_url = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# SQLModel engine
engine = create_engine(sql_url, echo=True)
