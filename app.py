import json

from chalice import Chalice, Response

from chalicelib.event_poll import dispatcher, TypeDiverge
from chalicelib.event_message_changed import attachment_main
from chalicelib.event_bot_message import geek_news_main

app = Chalice(app_name='secretary')


@app.route('/event_poll', methods=['POST'])
def event_poll():
    request = app.current_request.to_dict()
    json_body = app.current_request.json_body
    print(request)
    if request['headers'].get('x-slack-no-retry'):
        return Response(body='retry', headers={'X-Slack-No-Retry': '1'})
    print(json_body)
    result = dispatcher(TypeDiverge, json_body, 'type')
    print('result:', result)
    return Response(body=result, headers={'Content-Type': 'application/json', 'X-Slack-No-Retry': '1'})


@app.lambda_function(name='event_message_changed')
def event_message_changed(event, context):
    attachment_main(event)


@app.lambda_function(name='event_bot_message')
def event_bot_message(event, context):
    geek_news_main(event)
