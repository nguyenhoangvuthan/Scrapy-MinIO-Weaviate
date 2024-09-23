# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import io

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from minio import Minio, S3Error
#
#
def write_file_to_minio(bucket_name: str, file_name: str, line_as_bytes: bytes):
    client = Minio(
        "127.0.0.1:9000",
        access_key="lWbO5FrsFcp6xC04aqgy",
        secret_key="amwk7ARIFBhwfn8uix4HGXVq048laDzoaG96gL72",
        secure=False
    )
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket {bucket_name} created.")
        else:
            print(f"Bucket {bucket_name} already exists.")
    except S3Error as e:
        print(f"Error occurred while checking/creating bucket: {e}")

    # Create a BytesIO stream from the bytes
    line_as_a_stream = io.BytesIO(line_as_bytes)

    try:
        # Upload to MinIO
        client.put_object(
            bucket_name,
            file_name,
            line_as_a_stream,
            length=len(line_as_bytes)
        )
        print(f"Successfully uploaded {file_name} to {bucket_name}.")
    except S3Error as e:
        print(f"Error occurred while uploading to MinIO: {e}")


class QuotestoscrapePipeline:
    def __init__(self):
        self.items = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        combined_data = ''.join(self.items).encode('utf-8')
        write_file_to_minio(
            bucket_name="test-minio-nhvthan",
            file_name="my_file_latest.txt",
            line_as_bytes=combined_data
        )

    def process_item(self, item, spider):
            # Convert the item to a string and write it to the file
            line = f"Quote: {item.get('quote')}\n" \
                   f"Author: {item.get('author')}\n" \
                   f"Author About Link: {item.get('author_about_link')}\n" \
                   f"Tags: {', '.join(item.get('tags', []))}\n" \
                   f"Author Born Date: {item.get('author_born_date')}\n" \
                   f"Author Born Location: {item.get('author_born_location')}\n" \
                   f"\n"  # Add an empty line between items
            self.items.append(line)  # Store the line instead of writing immediately
            return item


