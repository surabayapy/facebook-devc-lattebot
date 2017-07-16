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
page.greeting('Hai {{user_first_name}}, bagaimana kabar kamu?!. Mau tau tentang Surabaya.py')
page.show_starting_button('GET_STARTED_BOT')
page.show_persistent_menu([
    {
        "locale": "default",
        "composer_input_disabled": False,
        "call_to_actions": [
            {
                "title": "My Account",
                "type": "nested",
                "call_to_actions": [
                    {
                        "title": "Pay Bill",
                        "type": "postback",
                        "payload": "PAYBILL_PAYLOAD"
                    },
                    {
                        "title": "History",
                        "type": "postback",
                        "payload": "HISTORY_PAYLOAD"
                    },
                    {
                        "title": "Contact Info",
                        "type": "postback",
                        "payload": "CONTACT_INFO_PAYLOAD"
                    }
                ]
            },
            {
                "type": "web_url",
                "title": "Latest News",
                "url": "http://petershats.parseapp.com/hat-news",
                "webview_height_ratio": "full"
            }
        ]
    },
    {
        "locale": "zh_CN",
        "composer_input_disabled": False
    }
])


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

    page.handle_webhook(_.json, received_message, received_postback)

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

    page.send(sender_id, 'ok dari kami')


def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    log.info("Received postback for user %s and page %s with payload '%s' at %s"
             % (sender_id, recipient_id, payload, time_of_postback))

    page.send(sender_id, "Postback called")