import logging

from google.cloud import storage
import os
from google.cloud import bigquery


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
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    logging.info("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


def gcs_to_bq(file:str):
    """from cloud storage to bigquery"""
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json('tmp/gcp_acc.json')
    table_id = "testing.parser"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("tag", "STRING"),
            bigquery.SchemaField("author", "STRING"),
            bigquery.SchemaField("quote", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = "gs://parser/json/" + file
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.
    load_job.result()  # Waits for the job to complete.
    destination_table = client.get_table(table_id)  # Make an API request.
    logging.info("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == '__main__':
    # list_of_files = os.listdir("/tmp/parser/")
    # print(list_of_files, type(list_of_files))
    # for file in list_of_files:
    #     print(f'uploading {file}')
    #     upload_to_cloud("parser", "/tmp/parser/" + file, file)
    gcs_to_bq()
