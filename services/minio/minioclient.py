import io
from minio import Minio, S3Error
from common.config import ClientConfig
from pydantic import BaseModel, Field


class MinioClient(BaseModel):
    config: ClientConfig = Field(default_factory=ClientConfig)

    @property
    def client(self):
        return Minio(
            endpoint=self.config.minio_endpoint,
            access_key=self.config.minio_access_key,
            secret_key=self.config.minio_secret_key,
            secure=False
        )

    def check_and_make_bucket(self, bucket_name: str):
        if not self.client.bucket_exists(bucket_name):
            try:
                self.client.make_bucket(bucket_name)
                return {
                    "Status": "Success",
                    "Message": "Create Bucket Successful"
                }
            except S3Error as e:
                return {
                    "Status": "Create Bucket Failed",
                    "Message": e.message
                }


    def upload_file_to_minio(self, bucket_name: str, file_name: str, data_as_byte: bytes, data: io.BytesIO) -> dict:
        try:
            # Upload to MinIO
            self.client.put_object(bucket_name, file_name, data, length=len(data_as_byte))
            return {
                "Status": "Success",
                "Message": "Upload File Successful"
            }
        except S3Error as e:
                return {
                    "Status": "Upload File Failed",
                    "Message": e.message
                }