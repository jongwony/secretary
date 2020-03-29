from lambda_function import event_poll


def test_msg():
    body = {'token': 'FcLrpGmG3VeCuyd7bUMQszKz', 'team_id': 'T48RY2MFH', 'api_app_id': 'ABRRHSHHU',
            'event': {'client_msg_id': 'cf450427-50da-46cf-8f08-64d797000fe5', 'type': 'message', 'text': 'asdfasdf',
                      'user': 'U78RDCCJE', 'ts': '1585462244.003200', 'team': 'T48RY2MFH', 'blocks': [
                    {'type': 'rich_text', 'block_id': 'uqCH',
                     'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'asdfasdf'}]}]}],
                      'channel': 'CGK4QNXNC', 'event_ts': '1585462244.003200', 'channel_type': 'channel'},
            'type': 'event_callback', 'event_id': 'Ev0111FLKTFY', 'event_time': 1585462244, 'authed_users': ['UU42MN82Y']}
    event_poll.main({}, body)


def test_error():
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate', 'CloudFront-Forwarded-Proto': 'https',
               'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false',
               'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false',
               'CloudFront-Viewer-Country': 'US', 'Content-Type': 'application/json',
               'Host': 'xvyryyt8fk.execute-api.ap-northeast-2.amazonaws.com',
               'User-Agent': 'Slackbot 1.0 (+https://api.slack.com/robots)',
               'Via': '1.1 077b94dab77b8114aebf503be197d7d9.cloudfront.net (CloudFront)',
               'X-Amz-Cf-Id': '9T1y1PfO8ESSk4Ejmt-ar7qKw52jIYF7dLmpw9_qyHCHThKI03oRLw==',
               'X-Amzn-Trace-Id': 'Root=1-5e803be8-d6426c6aa518b28cd9418db1', 'X-Forwarded-For': '3.95.168.245, 130.176.98.131',
               'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'X-Slack-Request-Timestamp': '1585462247',
               'X-Slack-Retry-Num': '1', 'X-Slack-Retry-Reason': 'http_error',
               'X-Slack-Signature': 'v0=1c7158802a71be161fa9ad0ff8cd4c7976f58d9c7e6cd6a98041821aa5241b42'}
    event_poll.main(headers, {})


def test_attachments(monkeypatch):
    def dummy_func(*args, **kwargs):
        return

    monkeypatch.setattr(event_poll, 'nosql_body_dump', dummy_func)
    monkeypatch.setattr(event_poll, 'integrity_check', dummy_func)

    body = {'token': 'FcLrpGmG3VeCuyd7bUMQszKz', 'team_id': 'T48RY2MFH', 'api_app_id': 'ABRRHSHHU',
            'event': {'type': 'message', 'subtype': 'message_changed', 'hidden': True,
                      'message': {'client_msg_id': 'd1921061-3cbe-42c0-8ce6-92ca8c393874', 'type': 'message',
                                  'text': '<https://mingrammer.com/translation-asynchronous-python/>', 'user': 'U78RDCCJE',
                                  'team': 'T48RY2MFH', 'attachments': [
                              {'title': '[번역] 비동기 파이썬', 'title_link': 'https://mingrammer.com/translation-asynchronous-python/',
                               'text': 'Asynchronous Python을 번역한 글입니다. 파이썬에서의 비동기 프로그래밍은 최근 점점 더 많은 인기를 끌고있다. 비동기 프로그래밍을 위한 파이썬 라이브러리는 많다. 그',
                               'fallback': '[번역] 비동기 파이썬', 'ts': 1475452800,
                               'from_url': 'https://mingrammer.com/translation-asynchronous-python/',
                               'service_icon': 'https://mingrammer.com/images/favicon.ico', 'service_name': 'mingrammer.com',
                               'id': 1, 'original_url': 'https://mingrammer.com/translation-asynchronous-python/'}], 'blocks': [
                              {'type': 'rich_text', 'block_id': 'wQ8n', 'elements': [{'type': 'rich_text_section', 'elements': [
                                  {'type': 'link', 'url': 'https://mingrammer.com/translation-asynchronous-python/'}]}]}],
                                  'ts': '1585461761.002500'}, 'channel': 'CGK4QNXNC',
                      'previous_message': {'client_msg_id': 'd1921061-3cbe-42c0-8ce6-92ca8c393874', 'type': 'message',
                                           'text': '<https://mingrammer.com/translation-asynchronous-python/>',
                                           'user': 'U78RDCCJE', 'ts': '1585461761.002500', 'team': 'T48RY2MFH', 'blocks': [
                              {'type': 'rich_text', 'block_id': 'wQ8n', 'elements': [{'type': 'rich_text_section', 'elements': [
                                  {'type': 'link', 'url': 'https://mingrammer.com/translation-asynchronous-python/'}]}]}]},
                      'event_ts': '1585461762.002600', 'ts': '1585461762.002600', 'channel_type': 'channel'},
            'type': 'event_callback', 'event_id': 'Ev0111FHUP4N', 'event_time': 1585461762, 'authed_users': ['UU42MN82Y']}
    event_poll.main({}, body)
