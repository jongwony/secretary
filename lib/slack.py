import json

from slacker import Slacker

from .connector import get_parameter


class AttachmentBuilder:
    def __init__(self):
        self.attachments = []

    def __call__(self):
        self.make_default()
        return json.dumps(self.attachments)

    def mod_fallback(self, fallback, index=0):
        try:
            self.attachments[index]['fallback'] = fallback
        except IndexError:
            self.attachments.append({'fallback': fallback})

    def mod_text(self, text, index=0):
        try:
            self.attachments[index]['text'] = text
        except IndexError:
            self.attachments.append({'text': text})

    def add_fields(self, title, value, short=False):
        new_att = []
        for att in self.attachments:
            # inject fields
            if att.get('fields') is None:
                att['fields'] = []
            att['fields'].append({'title': title, 'value': value, 'short': short})
            new_att.append(att)
        self.attachments = new_att

    def add_custom(self, data: dict):
        self.attachments.append(data)

    def make_default(self):
        new_att = []
        for att in self.attachments:
            # inject requirements
            if att.get('fallback') is None:
                att['fallback'] = ' '
            if att.get('text') is None:
                att['text'] = ' '
            new_att.append(att)
        self.attachments = new_att


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
        self.slack = Slacker(Slack.get_bot_user_oauth_token())
        self.channel = channel
        self.username = username

    def post_message(self, text=None, channel=None, username=None, attachments=None, mention=False):
        self.slack.chat.post_message(
            text=text,
            channel=channel or self.channel,
            username=username or self.username,
            attachments=attachments,
            link_names=int(mention)
        )

    def command(self, channel=None, command=None, text=None):
        self.slack.chat.command(
            channel=channel or self.channel,
            command=command,
            text=text,
        )
