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

# Other Constants
SECRET_KEY = os.getenv("SECRET_KEY", "your-open-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30