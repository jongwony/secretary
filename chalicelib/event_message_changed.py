import requests
import jmespath
from bs4 import BeautifulSoup

from chalicelib.core.io import integrity_check, is_geek_news


def attachment_main(event):
    print(event)

    channel = jmespath.search('event.channel', event)
    user, origin_text = jmespath.search('event | message.[user, text] || [user, text]', event)
    attachments = jmespath.search('event.message.attachments[].[title_link, title, text]', event) or []
    blocks = jmespath.search('event.message.blocks[] || event.blocks[]', event)
    urls = jmespath.search('[].elements[].elements[].url', blocks) or []

    if user == 'UU42MN82Y':
        # secretary bot
        return

    if not attachments:
        return

    for url, title, text in attachments:
        if m := is_geek_news(url):
            resp = requests.get(m.group())
            soup = BeautifulSoup(resp.content, 'html.parser')
            origin_a = soup.select_one('td.topictitle a')
            origin_url = origin_a.attrs.get('href')
            integrity_check(
                origin_url,
                channel,
                user=user,
                title=title,
                text=text,
                geek_news_id=m.group(1),
            )
        else:
            integrity_check(url, channel, user=user, title=title, text=text, origin_text=origin_text)

    if diff_set := set(urls) - set(x[0] for x in attachments):
        for url in diff_set:
            integrity_check(url, channel, user=user, origin_text=origin_text)
