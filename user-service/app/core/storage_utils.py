import boto3
from fastapi import UploadFile


async def upload_file_to_s3(file: UploadFile, file_name: str, backend) -> str:
    endpoint_url = backend.aws_host
    aws_access_key = backend.aws_access_key_id
    aws_secret_key = backend.aws_secret_access_key
    region_name = backend.aws_region
    bucket_name = backend.aws_bucket

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name,
    )

    file.file.seek(0)
    s3_client.upload_fileobj(file.file, bucket_name, file_name)

    base_url = endpoint_url.rstrip("/")
    return f"{base_url}/{bucket_name}/{file_name}"


def compute_human_file_size(file_instance):
    if not hasattr(file_instance, "file_size") or not file_instance.file_size:
        return
    size = file_instance.file_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            file_instance.human_file_size = f"{size:.2f} {unit}"
            return
        size /= 1024
    file_instance.human_file_size = f"{size:.2f} TB"
