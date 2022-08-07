import jmespath

from chalicelib.core.io import integrity_check


def attachment_main(event):
    channel = jmespath.search('event.channel', event)
    user, origin_text = jmespath.search('event | message.[user, text] || [user, text]', event)
    attachments = jmespath.search('event.message.attachments[].[title_link, title, text]', event) or []
    blocks = jmespath.search('event.message.blocks[] || event.blocks[]', event)
    urls = jmespath.search('[].elements[].elements[].url', blocks) or []

    if not attachments:
        return

    for url, title, text in attachments:
        integrity_check(url, channel, user=user, title=title, text=text, origin_text=origin_text)

    if diff_set := set(urls) - set(x[0] for x in attachments):
        for url in diff_set:
            integrity_check(url, channel, user=user, origin_text=origin_text)
