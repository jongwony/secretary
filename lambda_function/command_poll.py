import re
from urllib.parse import parse_qs

import jmespath
from pymysql.err import MySQLError

from lib.slack import Slack
from lib.connector import rdb_connector
from lib.io import raw_query


def slack_escape(s):
    rep = {'&': '&amp', '<': '&lt', '>': '&gt'}
    pattern = re.compile(r'[&<>]')
    return pattern.sub(lambda m: rep[m.group(0)], s)


def serial_yield(engine):
    for d in raw_query(engine, 'select * from dev_restrict'):
        yield f"<{d['url']}|{d['title']}> <!date^{int(d['create_date'].timestamp())}^Posted {{date_num}} {{time_secs}}|Posted 2014-02-18 6:39:42 AM PST>"


def pretty_payload(engine):
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
                        "text": s
                    }
                } for s in serial_yield(engine)]
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


def lambda_handler(event, context):
    """
    https://api.slack.com/interactivity/slash-commands
    """
    print(f'{event=}')
    body = parse_qs(event['body'])
    command = body['text'][0]
    engine = rdb_connector('/aurora/serverless', 'secretary')
    if command == 'database':
        payload = pretty_payload(engine)
    else:
        payload = None
    print(f'{payload=}')
    return Slack.server_response(200, body=payload)
