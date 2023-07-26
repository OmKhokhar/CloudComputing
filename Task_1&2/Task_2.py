import io
import boto3
import json
import requests

with open('a1.json', 'r') as file:
    data = json.load(file)

s3 = boto3.client('s3')

for item in data['songs']:
    img_url = item['img_url']
    artist_name = item['artist']
    img_filename = artist_name + '.jpg'
    response = requests.get(img_url)

    if response.status_code == 200:
        s3.upload_fileobj(io.BytesIO(response.content), 's3886577', img_filename)
        print(f"{img_filename} uploaded to S3 successfully.")
    else:
        print(f"Failed to download {img_filename}.")