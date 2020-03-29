from contextlib import contextmanager

from pymysql.cursors import SSDictCursor


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
