import json

import boto3
import jmespath
from sqlalchemy.exc import IntegrityError

from common.slack import Slack
from common.connector import rdb_connector

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
ssm = boto3.client('ssm', region_name='ap-northeast-2')
engine = rdb_connector('/aurora/serverless', 'secretary')


def get_parameter(name):
    return str(ssm.get_parameter(Name=name)['Parameter']['Value'])


def nosql_body_dump(body):
    nosql_table = dynamodb.Table('secretary')
    return nosql_table.put_item(Item=body)


def rdb_dump(client_msg_id, url, title, user, channel):
    return engine.execute(
        'INSERT INTO dev_restrict(id, url, title, user, channel) VALUES (%s, %s, %s, %s, %s)',
        [client_msg_id, url, title, user, channel],
    )


def integrity_check(client_msg_id, url, title, user, channel):
    def post_slack():
        bot = Slack()
        bot.post_message(text=f'중복 url: {url}', channel=channel, username='Link Crawler')

    try:
        rdb_dump(client_msg_id, url, title, user, channel)
        print(f'rdb: {url} dumped')
    except IntegrityError:
        post_slack()


def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(f'{body=}')

    channel = jmespath.search('event.channel', body)
    user, client_msg_id = jmespath.search('event | message.[user, client_msg_id] || [user, client_msg_id]', body)
    attachments = jmespath.search('event.message.attachments.[from_url, title]', body) or []

    blocks = jmespath.search('event.message.blocks[] || event.blocks[]', body)
    urls = jmespath.search('[].elements[].elements[].url', blocks) or []
    print(f'{urls=}')
    if not urls:
        return

    # rdb dump
    for url, title in attachments:
        integrity_check(client_msg_id, url, title, user, channel)

    if diff_set := set(urls) - set(x[0] for x in attachments):
        print(f'{diff_set=}')
        for url in diff_set:
            integrity_check(client_msg_id, url, None, user, channel)

        # nosql dump
        body['id'] = client_msg_id
        nosql_body_dump(body)
        print('dynamodb dumped')

    # test handshake response
    return {
        'statusCode': 200,
        'headers': {"content-type": "text/plain", 'X-Slack-No-Retry': 1},
        'body': body.get('challenge'),
    }
