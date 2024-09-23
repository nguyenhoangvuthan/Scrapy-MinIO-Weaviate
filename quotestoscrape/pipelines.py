# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import io
import os
from dotenv import load_dotenv
from pathlib import Path
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from common.config import ClientConfig
from services.minio.minioclient import MinioClient

#
def write_file_to_minio(minio_client: MinioClient, bucket_name: str, file_name: str, line_as_bytes: bytes):
    minio_client.check_and_make_bucket(bucket_name)

    # Create a BytesIO stream from the bytes
    line_as_a_stream = io.BytesIO(line_as_bytes)

    minio_client.upload_file_to_minio(bucket_name, file_name, line_as_bytes, line_as_a_stream)


class QuotestoscrapePipeline:
    def __init__(self):
        self.items = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        dotenv_path = Path('.dev.env')
        load_dotenv(dotenv_path=dotenv_path)

        minio_client: MinioClient = MinioClient(
            config=ClientConfig(
                minio_access_key= os.getenv('MINIO_ACCESS_KEY'),
                minio_secret_key = os.getenv('MINIO_SECRET_KEY')
            )
        )
        print("minio_client: ", minio_client)
        combined_data = ''.join(self.items).encode('utf-8')
        write_file_to_minio(minio_client, 'quotestoscrape', 'data', combined_data)

    def process_item(self, item, spider):
        # Convert the item to a dictionary using ItemAdapter
        item_dict = ItemAdapter(item).asdict()

        # Process the item
        quote = item_dict.get('quote')
        author = item_dict.get('author')
        author_about_link = item_dict.get('author_about_link')
        tags = item_dict.get('tags', [])
        author_born_date = item_dict.get('author_born_date')
        author_born_location = item_dict.get('author_born_location')

        line = f"Quote: {quote}\n" \
               f"Author: {author}\n" \
               f"Author About Link: {author_about_link}\n" \
               f"Tags: {', '.join(tags)}\n" \
               f"Author Born Date: {author_born_date}\n" \
               f"Author Born Location: {author_born_location}\n" \
               f"\n"

        self.items.append(line)
        return item


