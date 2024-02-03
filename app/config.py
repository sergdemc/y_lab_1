import os

from dotenv import load_dotenv

load_dotenv()

DB_USER: str = os.getenv('DB_USER')
DB_PASSWORD: str = os.getenv('DB_PASSWORD')
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')
DB_NAME: str = os.getenv('DB_NAME')

PORT: int = int(os.getenv('PORT', 8000))

POSTGRES_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

REDIS_SERVER: str = os.environ.get("REDIS_SERVER")
REDIS_PORT: int = int(os.environ.get("REDIS_PORT"))
