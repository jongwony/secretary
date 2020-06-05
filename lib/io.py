from datetime import datetime
from contextlib import contextmanager

import boto3
from pymysql.cursors import SSDictCursor

from .slack import Slack


def sql_streaming(sql, connector):
    """
    sql 문을 스트리밍 할 수 있습니다.
    for 문으로 이 함수를 받아서 쓴다면 메모리를 아주 효율적으로 아낄 수 있습니다.

    :param sql: sql statements
    :param connector: pymysql/sqlalchemy engine
    :return: generator
    """
    with SSDictCursor(connector) as cursor:
        cursor.execute(sql)
        yield from cursor.fetchall_unbuffered()


@contextmanager
def raw_connection(engine):
    connection = engine.raw_connection()
    yield connection
    connection.close()


def raw_query(engine, query):
    with raw_connection(engine) as conn:
        yield from sql_streaming(query, conn)


def nosql_body_dump(body):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')
    return nosql_table.put_item(Item=body)


def integrity_check(url, channel, **kwargs):
    def post_slack():
        bot = Slack()
        bot.post_message(text=f'중복 url: {url}', channel=channel, username='Link Crawler')

    data = {
        'id': url,
        'channel': channel,
        'timestamp': datetime.now().isoformat(),
        **kwargs
    }
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')

    try:
        response = nosql_table.get_item(Key={'id': url})
        assert response.get('Item') is None
    except AssertionError as e:
        print(e, url)
        post_slack()
    else:
        nosql_body_dump(data)
