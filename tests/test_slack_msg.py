import boto3


def test_dynamodb_exists():
    """
    return response
    response['Item'] = {
        'timestamp': '2020-07-21T01:50:12.911493',
        'geek_news_id': '2493',
        'text': '- 지메일에 Chat/Rooms/Meet 탭이 추가되고 모든 커뮤니케이션을 하나로 \n- 얼리억세스로 공개한뒤 올해안에 모든 G-Suite 사용자 대상으로 확대 에정\n- 메일부터 시작해서 File(Docs)/Task/Chat/Meet를 하나로 통합하는 작업환경으로 변화\n- 모바일/데스크탑 모두 지원 ',
        'id': 'https://www.theverge.com/2020/7/15/21325966/google-gmail-g-suite-chat-rooms-meet-integration-redesign',
        'channel': 'C010J11D5V3',
        'title': '[GeekNews] G-Suite용 Gmail, 채팅/대화방/화상통화 기능 추가 예정 '
    }
    """
    url = 'https://www.theverge.com/2020/7/15/21325966/google-gmail-g-suite-chat-rooms-meet-integration-redesign'

    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    nosql_table = dynamodb.Table('secretary')

    return nosql_table.get_item(Key={'id': url})
