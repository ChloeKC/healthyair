# HealthyAir - Google Cloud Utilities

from google.cloud import storage

from src.gcs_config import (
    PROJECT_ID,
    BUCKET_NAME,
    LOCATION
)


def get_storage_client(
    project_id=PROJECT_ID
):
    """
    Create GCS client using
    Application Default Credentials.
    """
    return storage.Client(
        project=project_id
    )


def create_gcs_bucket(
    bucket_name=BUCKET_NAME,
    project_id=PROJECT_ID,
    location=LOCATION,
):

    client = get_storage_client(
        project_id
    )

    bucket = client.lookup_bucket(
        bucket_name
    )

    if bucket:
        print(
            f"Bucket already exists: "
            f"gs://{bucket_name}"
        )
        return bucket

    bucket = client.bucket(
        bucket_name
    )

    bucket = client.create_bucket(
        bucket,
        location=location
    )

    print(
        f"Created bucket: "
        f"gs://{bucket_name}"
    )

    return bucket


def upload_file_to_gcs(
    local_path,
    destination_blob_name,
    bucket_name=BUCKET_NAME,
    project_id=PROJECT_ID,
):

    client = get_storage_client(
        project_id
    )

    bucket = client.bucket(
        bucket_name
    )

    blob = bucket.blob(
        destination_blob_name
    )

    blob.upload_from_filename(
        str(local_path)
    )

    print(
        f"Uploaded {local_path} "
        f"to gs://{bucket_name}/"
        f"{destination_blob_name}"
    )

# Upload Raw Dataset
# -------------------------------------------------------------------

def upload_raw_data():
    upload_file_to_gcs(
        local_path=RAW_FILE,
        destination_blob_name=RAW_GCS_PATH
    )

def list_bucket_contents(
    bucket_name=BUCKET_NAME,
    project_id=PROJECT_ID,
):

    client = get_storage_client(
        project_id
    )

    for blob in client.list_blobs(
        bucket_name
    ):
        print(blob.name)