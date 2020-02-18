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
    def __init__(self, channel=None, username=None):
        self.slack = Slacker(get_parameter('/dev_restrict/slack'))
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
