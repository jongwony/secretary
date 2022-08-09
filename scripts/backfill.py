import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from chalicelib.core.io import nosql_body_dump


def fetch(geek_news_id):
    target = f'https://news.hada.io/topic?id={geek_news_id}'
    resp = requests.get(target)
    soup = BeautifulSoup(resp.content, 'html.parser')
    try:
        title = soup.select_one('td.topictitle h1').get_text(strip=True)
    except AttributeError:
        print('NotFound', geek_news_id)
        return
    topic_info = soup.select_one('tr.topicinfo').get_text(strip=True)
    from_date = re.search(r'\d{4}-\d{2}-\d{2}', topic_info)
    timestamp = datetime.strptime(from_date.group(), '%Y-%m-%d').isoformat()
    try:
        text = soup.select_one('#topic_contents p').get_text()
    except AttributeError:
        text = None
    origin_a = soup.select_one('td.topictitle a')
    origin_url = origin_a.attrs.get('href')
    data = {
        'id': origin_url,
        'timestamp': timestamp,
        'title': title,
        'text': text,
        'geek_news_id': geek_news_id,
    }
    nosql_body_dump(data)
    print(origin_url)


def main():
    for x in range(2, 2215):
        fetch(x)


if __name__ == '__main__':
    main()
