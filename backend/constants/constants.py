import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Bucket Constants
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_HOST = os.getenv("MINIO_HOST")

# Database constants
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# TIDB Constants
TIDB_HOST = os.getenv('TIDB_HOST', 'localhost')
TIDB_PORT = os.getenv('TIDB_PORT', '4000')
TIDB_USERNAME = os.getenv('TIDB_USERNAME', 'root')
TIDB_PASSWORD = os.getenv('TIDB_PASSWORD', 'mypass')
TIDB_DB_NAME = os.getenv('TIDB_DATABASE', 'test')
TIDB_TABLE_NAME = os.getenv('TIDB_TABLENAME', 'product')

TEXT_EMBEDDING_DIM = 768
IMAGE_EMBEDDING_DIM = 512

# Other Constants
SECRET_KEY = os.getenv("SECRET_KEY", "your-open-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30