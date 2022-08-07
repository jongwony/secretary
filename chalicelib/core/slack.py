import json
from operator import attrgetter

from slacker import Slacker

from chalicelib.core.connector import get_parameter


class Slack:
    ssm_prefix = '/api_key/slack/dev_restrict/secretary'

    @classmethod
    def get_signing_secret(cls):
        return get_parameter(f'{cls.ssm_prefix}/signing_secret')

    @classmethod
    def get_bot_user_oauth_token(cls):
        return get_parameter(f'{cls.ssm_prefix}/bot_user_oauth_access_token')

    @classmethod
    def verification_requests(cls, headers, body):
        """
        https://api.slack.com/docs/verifying-requests-from-slack#signing_secrets_admin_page
        Example works... but Handshake NOT Works...
        """
        import hmac
        import hashlib
        from time import time
        from urllib.parse import urlencode

        slack_signing_secret = cls.get_signing_secret()
        timestamp = headers['X-Slack-Request-Timestamp']
        origin_signature = headers['X-Slack-Signature']

        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        if abs(int(time()) - int(timestamp)) > 60 * 5:
            return False

        sig_basestring = f'v0:{timestamp}:{urlencode(body)}'
        request_hash = hmac.new(
            slack_signing_secret.encode(),
            msg=sig_basestring.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        calc_signature = f'v0={request_hash}'

        print(origin_signature, calc_signature)

        return hmac.compare_digest(origin_signature, calc_signature)

    def __init__(self, channel=None, username=None):
        self.slack = Slacker(self.get_bot_user_oauth_token())
        self.channel = channel
        self.username = username

    def post_message(self, text=None, channel=None, username=None, blocks=None, attachments=None, mention=False):
        self.slack.chat.post_message(
            text=text,
            channel=channel or self.channel,
            username=username or self.username,
            blocks=blocks,
            attachments=attachments,
            link_names=int(mention)
        )

    def command(self, channel=None, command=None, text=None):
        self.slack.chat.command(
            channel=channel or self.channel,
            command=command,
            text=text,
        )

    def api(self, method, *args, **kwargs):
        return attrgetter(method)(self.slack)(*args, **kwargs)
