from minio import Minio
from minio.error import S3Error
from constants.constants import MINIO_BUCKET_NAME, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST

minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

bucket = MINIO_BUCKET_NAME

# Ensure the bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)