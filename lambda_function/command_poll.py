from urllib.parse import parse_qs

from lib.slack import Slack


def lambda_handler(event, context):
    """
    https://api.slack.com/interactivity/slash-commands
    """
    print(f'{event=}')
    body = parse_qs(event['body'])
    text = body['text']
    print(body)

    payload = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*It's 80 degrees right now.*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Partly cloudy today and tomorrow"
                }
            }
        ]
    }
    """
    {
      "response_type": "ephemeral",
      "text": "Sorry, that didn't work. Please try again."
    }
    """
    return Slack.server_response(200, body=payload)
