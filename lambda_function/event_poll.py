import json

import boto3
import jmespath
from sqlalchemy.exc import IntegrityError

from lib.connector import rdb_connector
from lib.slack import Slack


class TypeDiverge:
    @classmethod
    def url_verification(cls, headers, body):
        return {'challenge': body.get('challenge')}

    @classmethod
    def event_callback(cls, headers, body):
        return diverse(MessageTypeDiverge, headers, body, 'event.type')


class MessageTypeDiverge:
    @classmethod
    def message(cls, headers, body):
        return diverse(MessageSubtypeDiverge, headers, body, 'event.subtype')


class MessageSubtypeDiverge:
    @classmethod
    def message_changed(cls, headers, body):
        channel = jmespath.search('event.channel', body)
        user, client_msg_id = jmespath.search('event | message.[user, client_msg_id] || [user, client_msg_id]', body)
        attachments = jmespath.search('event.message.attachments[].[title_link, title]', body) or []
        blocks = jmespath.search('event.message.blocks[] || event.blocks[]', body)
        urls = jmespath.search('[].elements[].elements[].url', blocks) or []

        if not attachments:
            return

        print(f'{attachments=}')
        print(f'{urls=}')

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


def nosql_body_dump(body):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')
    return nosql_table.put_item(Item=body)


def rdb_dump(client_msg_id, url, title, user, channel):
    engine = rdb_connector('/aurora/serverless', 'secretary')
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


def diverse(cls, headers, body, query):
    query_diverge = getattr(cls, jmespath.search(query, body) or '', None)
    if callable(query_diverge):
        return query_diverge(headers, body)


def main(headers, body):
    # Slack Error
    if reason := headers.get('X-Slack-Retry-Reason'):
        print(reason)
        return Slack.server_response(500, headers={'X-Slack-No-Retry': 1})

    result = diverse(TypeDiverge, headers, body, 'type')
    print(result)
    return Slack.server_response(200, body=result)


def lambda_handler(event, context):
    body = json.loads(event.pop('body'))
    headers = event.pop('headers')

    print(f'{headers=}')
    print(f'{body=}')

    # TODO: async callback server_response
    return main(headers, body)