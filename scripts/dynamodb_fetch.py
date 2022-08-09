import boto3
import pandas as pd


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('secretary')

response = table.scan()
data = response['Items']
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
df = pd.DataFrame(data=data)
