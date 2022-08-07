import json

import boto3
import jmespath


class TypeDiverge:
    @classmethod
    def url_verification(cls, body):
        return body.get('challenge')

    @classmethod
    def event_callback(cls, body):
        return dispatcher(MessageTypeDiverge, body, 'event.type')


class MessageTypeDiverge:
    @classmethod
    def message(cls, body):
        return dispatcher(MessageSubtypeDiverge, body, 'event.subtype')


class MessageSubtypeDiverge:
    @classmethod
    def message_changed(cls, body):
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName='secretary-dev-event_message_changed',
            InvocationType='Event',
            Payload=json.dumps(body).encode()
        )
        return "success"

    @classmethod
    def bot_message(cls, body):
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName='secretary-dev-event_bot_message',
            InvocationType='Event',
            Payload=json.dumps(body).encode()
        )
        return "success"


def dispatcher(cls, body, query):
    query_diverge = getattr(cls, jmespath.search(query, body) or '', None)
    if callable(query_diverge):
        return query_diverge(body)
