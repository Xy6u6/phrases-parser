from google.cloud import storage
import os


def upload_to_cloud(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    storage_client = storage.Client.from_service_account_json('tmp/gcp_acc.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("json/" + destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


if __name__ == '__main__':
    list_of_files = os.listdir("/tmp/parser/")
    print(list_of_files, type(list_of_files))
    for file in list_of_files:
        print(f'uploading {file}')
        upload_to_cloud("parser", "/tmp/parser/" + file, file)
