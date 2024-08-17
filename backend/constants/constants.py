from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_HOST = os.getenv("MINIO_HOST")
