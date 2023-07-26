import urllib
import boto3
import requests
import os

AWS_ACCESS_KEY_ID = os.environ.get('my_key')
AWS_SECRET_ACCESS_KEY = os.environ.get('my_acc')
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'arcade'


def generate_presigned_url(file_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': file_name},
            ExpiresIn=3600,
        )
        return presigned_url
    except Exception as e:
        return print(f"Error generating pre-signed URL: {e}")


def upload_file_to_s3(presigned_url, file_content):
    try:
        response = requests.put(presigned_url, data=file_content)

        if response.status_code == 200:
            return True
        else:
            print(f"Error uploading file to S3: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error uploading file: {e}")
        return False


def get_image_url_from_s3(image_url):
    try:
        parsed_url = urllib.parse.urlparse(image_url)
        image_name = urllib.parse.unquote(parsed_url.path)


        s3_image_url = f"{image_name}"

        return s3_image_url
    except Exception as e:
        print(f"Error generating image URL: {e}")
        return None
