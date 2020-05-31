import json

import boto3
import jmespath

from lib.slack import Slack


def nosql_body_dump(body):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')
    return nosql_table.put_item(Item=body)


def integrity_check(url, channel, **kwargs):
    def post_slack():
        bot = Slack()
        bot.post_message(text=f'중복 url: {url}', channel=channel, username='Link Crawler')

    data = {
        'id': url,
        'channel': channel,
        **kwargs
    }
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')

    try:
        response = nosql_table.get_item(Key={'id': url})
        assert response.get('Item') is None
    except AssertionError as e:
        print(e, url)
        post_slack()
    else:
        nosql_body_dump(data)


def lambda_handler(event, context):
    body = json.loads(event.pop('body'))

    channel = jmespath.search('event.channel', body)
    user, origin_text = jmespath.search('event | message.[user, text] || [user, text]', body)
    attachments = jmespath.search('event.message.attachments[].[title_link, title, text]', body) or []
    blocks = jmespath.search('event.message.blocks[] || event.blocks[]', body)
    urls = jmespath.search('[].elements[].elements[].url', blocks) or []

    if not attachments:
        return

    for url, title, text in attachments:
        integrity_check(url, channel, user=user, title=title, text=text, origin_text=origin_text)

    if diff_set := set(urls) - set(x[0] for x in attachments):
        for url in diff_set:
            integrity_check(url, channel, user=user, origin_text=origin_text)
