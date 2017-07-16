# -*- coding: utf-8 -*-
"""
    Application Startup
    ~~~~~~~~~

    :author: nanang.jobs@gmail.com
    :copyright: (c) 2017 by Nanang Suryadi.
    :license: BSD, see LICENSE for more details.
    
    app.py
"""
from baka import Baka, log, settings as ENV
from .chat.page import Page

settings = {
    'env': [
        ENV.EnvSetting('verify_token', 'FB_VERIFY_TOKEN'),
        ENV.EnvSetting('access_token', 'FB_ACCESS_TOKEN'),
    ]
}

app = Baka(__name__, **settings)
settings = app.config.registry.settings

page = Page(settings.get('access_token'))


@app.route('/')
def index(_):

    return {'LatteBot': 'Surabaya.py dan Facebook DevC Surabaya'}


@app.route('/chat')
def validate(_):
    response = _.response
    if _.params.get('hub.mode', '') == 'subscribe' and _.params.get('hub.verify_token', '') \
            == settings.get('verify_token'):

        print("Validating webhook")

        response.status_code = 200
        return int(_.params.get('hub.challenge', ''))
    else:
        return 'Failed validation. Make sure the validation tokens match.'


@app.route('/chat', request_method='POST')
def webhook(_):
    log.info(_.json_body)
    log.info(_.body)
    log.info(_.json)

    page.handle_webhook(_.json, received_message)

    response = _.response
    response.status_code = 200

    return "OK"


app.scan()


def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    log.info("Received message for user %s and page %s at %s with message:"
             % (sender_id, recipient_id, time_of_message))
    log.info(message)
