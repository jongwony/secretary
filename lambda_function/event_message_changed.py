import json

import boto3
import jmespath

from lib.slack import Slack


def nosql_body_dump(body):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')
    return nosql_table.put_item(Item=body)


def integrity_check(client_msg_id, url, title, user, channel):
    def post_slack():
        bot = Slack()
        bot.post_message(text=f'중복 url: {url}', channel=channel, username='Link Crawler')

    data = {
        'id': url,
        'title': title,
        'user': user,
        'channel': channel,
        'client_msg_id': client_msg_id,
    }
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        nosql_table = dynamodb.Table('secretary')
        response = nosql_table.get_item(Key=data)
        assert response.get('Item') is not None
    except AssertionError:
        post_slack()
        nosql_body_dump(data)


def lambda_handler(event, context):
    body = json.loads(event.pop('body'))

    channel = jmespath.search('event.channel', body)
    user, client_msg_id = jmespath.search('event | message.[user, client_msg_id] || [user, client_msg_id]', body)
    attachments = jmespath.search('event.message.attachments[].[title_link, title]', body) or []
    blocks = jmespath.search('event.message.blocks[] || event.blocks[]', body)
    urls = jmespath.search('[].elements[].elements[].url', blocks) or []

    if not attachments:
        return

    for url, title in attachments:
        integrity_check(client_msg_id, url, title, user, channel)

    if diff_set := set(urls) - set(x[0] for x in attachments):
        for url in diff_set:
            integrity_check(client_msg_id, url, None, user, channel)
