import json

import jmespath

from lib.io import integrity_check


def attachment_main(body):
    channel = jmespath.search('event.channel', body)
    user, origin_text = jmespath.search('event | message.[user, text] || [user, text]', body)
    attachments = jmespath.search('event.message.attachments[].[title_link, title, text]', body) or []
    blocks = jmespath.search('event.message.blocks[] || event.blocks[]', body)
    urls = jmespath.search('[].elements[].elements[].url', blocks) or []

    if not attachments:
        return

    for url, title, text in attachments:
        integrity_check(url, channel, user=user, title=title, text=text, origin_text=origin_text)

    if diff_set := set(urls) - set(x[0] for x in attachments):
        for url in diff_set:
            integrity_check(url, channel, user=user, origin_text=origin_text)


def lambda_handler(event, context):
    body = json.loads(event.pop('body'))
    attachment_main(body)
