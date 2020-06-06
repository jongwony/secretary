import re
from datetime import datetime
from urllib.parse import parse_qs

import boto3
import jmespath
from pymysql.err import MySQLError

from lib.slack import Slack


def slack_escape(s):
    rep = {'&': '&amp', '<': '&lt', '>': '&gt'}
    pattern = re.compile(r'[&<>]')
    return pattern.sub(lambda m: rep[m.group(0)], s)


def serial_yield():
    def timestamp(date_string):
        try:
            return int(datetime.fromisoformat(date_string).timestamp())
        except (ValueError, TypeError):
            return None

    dynamodb = boto3.client('dynamodb')
    for d in dynamodb.scan(TableName='secretary')['Items']:
        parsed = jmespath.search(
            '{url: id.S, channel: channel.S,'
            'user: user.S title: title.S,'
            'timestamp: timestamp.S}', d)
        yield f"• <{parsed['url']}|{parsed['title']}>\n" \
              f"  origin channel: <#{parsed['channel']}>\n" \
              f"  origin user: {parsed['user']}\n" if parsed['user'] else '' \
              f"  <!date^{timestamp(parsed['timestamp'])}^Posted {{date_num}} {{time_secs}}|Posted 2014-02-18 6:39:42 AM PST>\n" if parsed['timestamp'] else ''


def pretty_payload():
    try:
        payload = {
            "response_type": "in_channel",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "text": "*Link Database.*",
                        "type": "mrkdwn"
                    },
                },
                *[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": s,
                    }
                } for s in serial_yield()]
            ]
        }
    except MySQLError as e:
        payload = {
            "response_type": "ephemeral",
            "text": f"Sorry, that didn't work. Please try again.\n{e.args}"
        }
    return payload


def slack_id_map():
    bot = Slack()
    channels = bot.api('conversations.list').body
    users = bot.api('users.list').body
    return {
        **dict(jmespath.search('members[][id, name]', users)),
        **dict(jmespath.search('channels[][id, name]', channels)),
    }


def command_main(body):
    """
    https://api.slack.com/interactivity/slash-commands
    """
    command = body['text'][0]
    if command == 'all link':
        payload = pretty_payload()
    elif command == 'query':
        payload = None
    else:
        payload = None
    return payload


def lambda_handler(event, context):
    body = parse_qs(event['body'])
    print(body)
    # TODO: timeout control
    return Slack.server_response(200, body=command_main(body))
