import json

import boto3
import jmespath
from sqlalchemy.exc import IntegrityError

from common.slack import Slack
from common.connector import rdb_connector

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
ssm = boto3.client('ssm', region_name='ap-northeast-2')
engine = rdb_connector('/aurora/serverless', 'secretary', echo=True)


def get_parameter(name):
    return str(ssm.get_parameter(Name=name)['Parameter']['Value'])


def nosql_body_dump(body):
    nosql_table = dynamodb.Table('secretary')
    return nosql_table.put_item(Item=body)


def rdb_dump(url, title):
    return engine.execute('''INSERT INTO dev_restrict(url, title) VALUES (%s, %s)''', [url, title])


def post_slack(token, channel, url):
    bot = Slack(token)
    bot.post_message(text=f'중복 url: {url}', channel=channel, username='Link Crawler')


def lambda_handler(event, context):
    body = json.loads(event['body'])
    try:
        token, team_id, api_app_id, channel = jmespath.search('[token, team_id, api_app_id, channel]', body)
        url, title = jmespath.search('event.message.attachments[0].[from_url, title]', body)
    except TypeError:
        return
    if not url:
        print('Not link')
        return

    # debug
    print(f'{event=}', f'{vars(context)=}')

    try:
        rdb_resp = rdb_dump(url, title)
        print('rdb dumped')
        print(vars(rdb_resp.context))
    except IntegrityError:
        post_slack(token, channel, url)
    else:
        body['id'] = engine.execute('SELECT LAST_INSERT_ID()').fetchone()[0]
        nosql_resp = nosql_body_dump(body)
        print('dynamodb dumped')
        print(vars(nosql_resp))

    # test handshake response
    return {
        'statusCode': 200,
        'headers': {"content-type": "text/plain"},
        'body': body.get('challenge')
    }
