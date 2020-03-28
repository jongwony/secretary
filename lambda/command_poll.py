import json

import boto3
import jmespath
from sqlalchemy.exc import IntegrityError

from lib.connector import rdb_connector
from urllib.parse import parse_qs
from lib.slack import Slack


def lambda_handler(event, context):
    """
    https://api.slack.com/interactivity/slash-commands
    """
    print(f'{event=}')
    parse_qs(event['body'])
    Slack.server_response(200, body={
        "response_type": "in_channel",
        "text": "It's 80 degrees right now."
    })
    """
    {
      "response_type": "ephemeral",
      "text": "Sorry, that didn't work. Please try again."
    }
    """
