import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
	TableName = 'music3',

	KeySchema = [
    	{
        	'AttributeName': 'artist',
        	'KeyType': 'HASH'
    	},
    	{
        	'AttributeName': 'title',
        	'KeyType': 'RANGE'
    	},
	],
	AttributeDefinitions = [
	{
        'AttributeName': 'artist',
        'AttributeType': 'S'
    	},
    	{
        	'AttributeName': 'title',
        	'AttributeType': 'S'
    	}
	],
	ProvisionedThroughput = {
    	'ReadCapacityUnits': 10,
    	'WriteCapacityUnits': 10
	}
)

table.wait_until_exists()