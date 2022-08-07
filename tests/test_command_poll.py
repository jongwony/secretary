from urllib.parse import parse_qs

from chalicelib import command_poll
from chalicelib.core.connector import rdb_connector


def test_do_database():
    event = {'resource': '/command_poll', 'path': '/command_poll', 'httpMethod': 'POST',
             'headers': {'Accept': 'application/json,*/*', 'Accept-Encoding': 'gzip,deflate',
                         'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true',
                         'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false',
                         'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'US',
                         'Content-Type': 'application/x-www-form-urlencoded',
                         'Host': 'hby6zd3tfb.execute-api.ap-northeast-2.amazonaws.com',
                         'User-Agent': 'Slackbot 1.0 (+https://api.slack.com/robots)',
                         'Via': '1.1 b4346add631a498bf6cdbf88cbc5ff13.cloudfront.net (CloudFront)',
                         'X-Amz-Cf-Id': '2g5SCSShN89OcK5vHzLtkkzenLIFKFox7Mq_NWToXvY2KoqLz8AbPQ==',
                         'X-Amzn-Trace-Id': 'Root=1-5e80e18f-38d259c056fd03a008b82408',
                         'X-Forwarded-For': '3.92.190.132, 70.132.33.131', 'X-Forwarded-Port': '443',
                         'X-Forwarded-Proto': 'https', 'X-Slack-Request-Timestamp': '1585504655',
                         'X-Slack-Signature': 'v0=f988beda3111abbc38f93fc77cabc1ef1e388ceb86976d619376071615227989'},
             'multiValueHeaders': {'Accept': ['application/json,*/*'], 'Accept-Encoding': ['gzip,deflate'],
                                   'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'],
                                   'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'],
                                   'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['US'],
                                   'Content-Type': ['application/x-www-form-urlencoded'],
                                   'Host': ['hby6zd3tfb.execute-api.ap-northeast-2.amazonaws.com'],
                                   'User-Agent': ['Slackbot 1.0 (+https://api.slack.com/robots)'],
                                   'Via': ['1.1 b4346add631a498bf6cdbf88cbc5ff13.cloudfront.net (CloudFront)'],
                                   'X-Amz-Cf-Id': ['2g5SCSShN89OcK5vHzLtkkzenLIFKFox7Mq_NWToXvY2KoqLz8AbPQ=='],
                                   'X-Amzn-Trace-Id': ['Root=1-5e80e18f-38d259c056fd03a008b82408'],
                                   'X-Forwarded-For': ['3.92.190.132, 70.132.33.131'], 'X-Forwarded-Port': ['443'],
                                   'X-Forwarded-Proto': ['https'], 'X-Slack-Request-Timestamp': ['1585504655'],
                                   'X-Slack-Signature': [
                                       'v0=f988beda3111abbc38f93fc77cabc1ef1e388ceb86976d619376071615227989']},
             'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None,
             'stageVariables': None,
             'requestContext': {'resourceId': 'ohs34g', 'resourcePath': '/command_poll', 'httpMethod': 'POST',
                                'extendedRequestId': 'KKgueFsyoE0FsQg=', 'requestTime': '29/Mar/2020:17:57:35 +0000',
                                'path': '/default/command_poll', 'accountId': '237943334087', 'protocol': 'HTTP/1.1',
                                'stage': 'default', 'domainPrefix': 'hby6zd3tfb', 'requestTimeEpoch': 1585504655743,
                                'requestId': 'e3dccfc3-bb61-4fe8-9543-4095955e3428',
                                'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None,
                                             'caller': None, 'sourceIp': '3.92.190.132', 'principalOrgId': None,
                                             'accessKey': None, 'cognitoAuthenticationType': None,
                                             'cognitoAuthenticationProvider': None, 'userArn': None,
                                             'userAgent': 'Slackbot 1.0 (+https://api.slack.com/robots)', 'user': None},
                                'domainName': 'hby6zd3tfb.execute-api.ap-northeast-2.amazonaws.com', 'apiId': 'hby6zd3tfb'},
             'body': 'token=FcLrpGmG3VeCuyd7bUMQszKz&team_id=T48RY2MFH&team_domain=restrictedzone&channel_id=CGK4QNXNC&channel_name=bot_test&user_id=U78RDCCJE&user_name=lastone9182&command=%2Fdo&text=database&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT48RY2MFH%2F1033997081888%2Fxq1GLzT5oTvlhwzh8LcS32BE&trigger_id=1022526359555.144882089527.1e133d245a2ad582ec2c1b04f504b94e',
             'isBase64Encoded': False}
    engine = rdb_connector('/aurora/serverless', 'secretary')
    payload = command_poll.pretty_payload(engine)
    print(payload)
    assert payload['response_type'] == 'in_channel'


def test_test():
    event = {'resource': '/command_poll', 'path': '/command_poll', 'httpMethod': 'POST',
             'headers': {'Accept': 'application/json,*/*', 'Accept-Encoding': 'gzip,deflate',
                         'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true',
                         'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false',
                         'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'US',
                         'Content-Type': 'application/x-www-form-urlencoded',
                         'Host': 'hby6zd3tfb.execute-api.ap-northeast-2.amazonaws.com',
                         'User-Agent': 'Slackbot 1.0 (+https://api.slack.com/robots)',
                         'Via': '1.1 841dfa6074cf4b3b0718988f088a4ac2.cloudfront.net (CloudFront)',
                         'X-Amz-Cf-Id': 'IC2X4uOD29Ib72SeEOcwH6dtDpZT1d4NcCSFMkINfy0a7fSnqNolGQ==',
                         'X-Amzn-Trace-Id': 'Root=1-5e80e3ac-b4135d0033b34f00a544ea40',
                         'X-Forwarded-For': '54.146.242.141, 70.132.33.81', 'X-Forwarded-Port': '443',
                         'X-Forwarded-Proto': 'https', 'X-Slack-Request-Timestamp': '1585505195',
                         'X-Slack-Signature': 'v0=3e13cc0c9068e66ec12306741be268bc34a1cd87ad0d725256c8c35dc65581d3'},
             'multiValueHeaders': {'Accept': ['application/json,*/*'], 'Accept-Encoding': ['gzip,deflate'],
                                   'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'],
                                   'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'],
                                   'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['US'],
                                   'Content-Type': ['application/x-www-form-urlencoded'],
                                   'Host': ['hby6zd3tfb.execute-api.ap-northeast-2.amazonaws.com'],
                                   'User-Agent': ['Slackbot 1.0 (+https://api.slack.com/robots)'],
                                   'Via': ['1.1 841dfa6074cf4b3b0718988f088a4ac2.cloudfront.net (CloudFront)'],
                                   'X-Amz-Cf-Id': ['IC2X4uOD29Ib72SeEOcwH6dtDpZT1d4NcCSFMkINfy0a7fSnqNolGQ=='],
                                   'X-Amzn-Trace-Id': ['Root=1-5e80e3ac-b4135d0033b34f00a544ea40'],
                                   'X-Forwarded-For': ['54.146.242.141, 70.132.33.81'], 'X-Forwarded-Port': ['443'],
                                   'X-Forwarded-Proto': ['https'], 'X-Slack-Request-Timestamp': ['1585505195'],
                                   'X-Slack-Signature': [
                                       'v0=3e13cc0c9068e66ec12306741be268bc34a1cd87ad0d725256c8c35dc65581d3']},
             'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None,
             'stageVariables': None,
             'requestContext': {'resourceId': 'ohs34g', 'resourcePath': '/command_poll', 'httpMethod': 'POST',
                                'extendedRequestId': 'KKiC9EaJoE0FRZg=', 'requestTime': '29/Mar/2020:18:06:36 +0000',
                                'path': '/default/command_poll', 'accountId': '237943334087', 'protocol': 'HTTP/1.1',
                                'stage': 'default', 'domainPrefix': 'hby6zd3tfb', 'requestTimeEpoch': 1585505196430,
                                'requestId': 'c5d85ac4-484e-4a35-bc6d-fe48139ae38a',
                                'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None,
                                             'caller': None, 'sourceIp': '54.146.242.141', 'principalOrgId': None,
                                             'accessKey': None, 'cognitoAuthenticationType': None,
                                             'cognitoAuthenticationProvider': None, 'userArn': None,
                                             'userAgent': 'Slackbot 1.0 (+https://api.slack.com/robots)', 'user': None},
                                'domainName': 'hby6zd3tfb.execute-api.ap-northeast-2.amazonaws.com', 'apiId': 'hby6zd3tfb'},
             'body': 'token=FcLrpGmG3VeCuyd7bUMQszKz&team_id=T48RY2MFH&team_domain=restrictedzone&channel_id=CGK4QNXNC&channel_name=bot_test&user_id=U78RDCCJE&user_name=lastone9182&command=%2Fdo&text=database&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT48RY2MFH%2F1022531726691%2FEd2UX7V59tqbPnjiyPE2ejW2&trigger_id=1036031200343.144882089527.a90cda519fc263d909b5d3a3ab839020',
             'isBase64Encoded': False}
    body = parse_qs(event['body'])
    command = body['text'][0]
    assert command == 'database'
