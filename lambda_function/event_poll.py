import json

import boto3
import jmespath
from lib.slack import Slack


class TypeDiverge:
    @classmethod
    def url_verification(cls, event):
        body = json.loads(event.get('body'))
        return {'challenge': body.get('challenge')}

    @classmethod
    def event_callback(cls, event):
        return dispatcher(MessageTypeDiverge, event, 'event.type')


class MessageTypeDiverge:
    @classmethod
    def message(cls, event):
        return dispatcher(MessageSubtypeDiverge, event, 'event.subtype')


class MessageSubtypeDiverge:
    @classmethod
    def message_changed(cls, event):
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName='event_message_changed',
            InvocationType='Event',
            Payload=json.dumps(event).encode()
        )


def dispatcher(cls, event, query):
    body = json.loads(event.get('body'))
    query_diverge = getattr(cls, jmespath.search(query, body) or '', None)
    if callable(query_diverge):
        return query_diverge(event)


def main(event):
    # Slack Error
    if reason := jmespath.search('headers."X-Slack-Retry-Reason"', event):
        print(reason)
        return Slack.server_response(500, headers={'X-Slack-No-Retry': 1})

    result = dispatcher(TypeDiverge, event, 'type')
    return Slack.server_response(200, body=result)


def lambda_handler(event, context):
    print(event.get('body'))
    return main(event)
