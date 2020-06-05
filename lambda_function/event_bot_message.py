import json
import re

import jmespath
import requests
from bs4 import BeautifulSoup

from lib.io import integrity_check


def geek_news_parser(body):
    return jmespath.search(
        'event.{'
        'channel: channel,'
        'title: text,'
        "link_block: blocks[?text.type == 'mrkdwn'] | [0].text.text,"
        "text_block : blocks[?text.type == 'plain_text'] | [0].text.text}", body
    )


def geek_news_validator(parsed):
    return re.search(r'https?://news.hada.io/topic\?id=(\d+)', parsed['link_block'])


def geek_news_main(body):
    parsed = geek_news_parser(body)
    if m := geek_news_validator(parsed):
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


def lambda_handler(event, context):
    body = json.loads(event.pop('body'))
    geek_news_main(body)
