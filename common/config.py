from pydantic import BaseModel, Field


class ClientConfig(BaseModel):
    minio_access_key_default: str = "minio"
    minio_secret_key_default: str = "minio123"
    minio_endpoint: str = Field(default="127.0.0.1:9000")
    minio_access_key: str = Field(default=minio_access_key_default)
    minio_secret_key: str = Field(default=minio_secret_key_default)
    weaviate_endpoint: str = Field(default="127.0.0.1:8081")