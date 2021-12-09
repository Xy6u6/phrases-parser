import logging

from google.cloud import storage
from google.cloud import bigquery

service_acc_key_path = 'tmp/gcp-acc.json'
gcs_bucket_path = "gs://parser/"
def upload_to_cloud(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json(service_acc_key_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    logging.info("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


def gcs_to_bq(file:str):
    """from cloud storage to bigquery"""
    client = bigquery.Client.from_service_account_json(service_acc_key_path)
    table_id = "testing.parser"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("tag", "STRING"),
            bigquery.SchemaField("author", "STRING"),
            bigquery.SchemaField("quote", "STRING"),
        ],
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = gcs_bucket_path + file
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )
    load_job.result()
    destination_table = client.get_table(table_id)
    logging.info("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == '__main__':
    gcs_to_bq()
