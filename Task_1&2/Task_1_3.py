import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

table_name = 'music3'

json_file_path = 'a1.json'

with open(json_file_path) as f:
    data = json.load(f)

for songs in data['songs']:
    item={
        'title': {'S': songs['title']},
        'artist': {'S': songs['artist']},
        'year': {'N': songs['year']},
        'web_url': {'S': songs['web_url']},
        'img_url': {'S': songs['img_url']}
    }
    print("Adding ", item)
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    print(response)