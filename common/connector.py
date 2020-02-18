from urllib.parse import urlencode

import boto3
import pymysql
import sqlalchemy as sa

ssm = boto3.client('ssm', region_name='ap-northeast-2')


def get_parameter(name):
    return str(ssm.get_parameter(Name=name)['Parameter']['Value'])


def rdb_connector(ssm_key, database, params=None, **prop):
    url_param = {'charset': 'utf8mb4'}
    if params is not None:
        url_param.update(params)

    return sa.create_engine(
        f'{get_parameter(ssm_key)}{database}?{urlencode(url_param)}',
        **prop
    )


def raw_rdb_connector(ssm_key, database):
    connect_dict = remote_str(ssm_key, database)
    connect_dict.update(
        db=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return pymysql.connect(**connect_dict)


def remote_str(ssm_key, database, charset='utf8mb4'):
    connect_str = get_parameter(ssm_key)
    connect_str = connect_str[connect_str.find('/'):].strip('/')
    [user, password], [host, port] = [x.split(':') for x in connect_str.split('@')]
    return {
        'user': user,
        'password': password,
        'host': host,
        'port': int(port),
        'database': database,
        'charset': charset,
    }
