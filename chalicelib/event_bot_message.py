import re

import jmespath
import requests
from bs4 import BeautifulSoup

from chalicelib.core.io import integrity_check, is_geek_news


def bot_request(event):
    return jmespath.search(
        'event.{'
        'channel: channel,'
        'title: text,'
        "link_block: blocks[?text.type == 'mrkdwn'] | [0].text.text,"
        "text_block : blocks[?text.type == 'plain_text'] | [0].text.text}", event
    )


def geek_news_validator(parsed):
    return re.search(r'https?://news.hada.io/topic\?id=(\d+)', parsed['link_block'])


def geek_news_main(event):
    parsed = bot_request(event)
    if m := is_geek_news(parsed['link_block']):
        resp = requests.get(m.group())
        soup = BeautifulSoup(resp.content, 'html.parser')
        origin_a = soup.select_one('td.topictitle a')
        origin_url = origin_a.attrs.get('href')
        integrity_check(
            origin_url,
            parsed['channel'],
            title=parsed['title'],
            text=parsed['text_block'],
            geek_news_id=m.group(1),
        )
