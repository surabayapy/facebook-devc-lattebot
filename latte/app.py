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
page.show_starting_button('USER_DEFINED_PAYLOAD')
page.show_persistent_menu([
    {
        "title": "Coffee Menu",
        "type": "nested",
        "call_to_actions": [
            {
                "title": "Cappuccino",
                "type": "postback",
                "payload": "CAPPUCCINO_PAYLOAD"
            },
            {
                "title": "Latte",
                "type": "postback",
                "payload": "LATTE_PAYLOAD"
            },
            {
                "title": "Mochaccino",
                "type": "postback",
                "payload": "MOCHACCINO_PAYLOAD"
            }
        ]
    },
    {
        "type": "web_url",
        "title": "WE ARE HIRING!",
        "url": "https://pinjam.co.id/perusahaan/karier",
        "webview_height_ratio": "full"
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

        log.info("Validating webhook")

        response.status_code = 200
        return int(_.params.get('hub.challenge', ''))
    else:
        return 'Failed validation. Make sure the validation tokens match.'


@app.route('/chat', request_method='POST')
def webhook(_):
    # log.info(_.json_body)
    # log.info(_.body)
    # log.info(_.json)

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

    if event.is_text_message:
        message_text = message.get("text")
        page.send(sender_id, 'ini pesan kamu: %s' % message_text)
        # send_message(sender_id, message_text)
    elif event.is_attachment_message:
        message_attachments = message.get("attachments")
        page.send(sender_id, "Message with attachment received")


def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    log.info("Received postback for user %s and page %s with payload '%s' at %s"
             % (sender_id, recipient_id, payload, time_of_postback))

    if 'USER_DEFINED_PAYLOAD' in payload:
        # ambil data profile user
        """
        {
            first_name: 'First name',
            last_name: 'Last name',
            profile_pic: 'Profile picture',
            locale: 'Locale of the user on Facebook',
            timezone: 'Timezone, number relative to GMT',
            gender: 'Gender',
            is_payment_enabled: 'Is the user eligible to receive messenger platform payment messages',
            last_ad_referral: 'Details of the last Messenger Conversation Ad user was referred from'
        }
        """
        user = page.get_user_profile(sender_id)

        page.send(sender_id, 'hi {}, selamat bergabung dengan kami Surabaya.py'.format(user['first_name']))
        return

    def coffee_menu(payload):

        if 'CAPPUCCINO_PAYLOAD' in payload:
            postback = {
                'type': 'template',
                'payload': {
                  'template_type': 'generic',
                  'elements': [{
                    'title': 'Cappuccino Coffee',
                    'subtitle': 'Sejarah Cappuccino',
                    'item_url': 'https://majalah.ottencoffee.co.id/sejarah-cappuccino/',
                    'image_url': 'https://majalah.ottencoffee.co.id/wp-content/uploads/2015/11/DSCF6342.jpg',
                    'buttons': [{
                      'type': 'web_url',
                      'url': "https://majalah.ottencoffee.co.id/sejarah-cappuccino/",
                      'title': "Selengkapnya"
                    }],
                  }]
                }
              }
            page.send(sender_id, postback)
            return

        if 'LATTE_PAYLOAD' in payload:
            postback = {
                'type': 'template',
                'payload': {
                  'template_type': 'generic',
                  'elements': [{
                    'title': 'Latte Coffee',
                    'subtitle': 'mencerup sejarah di cafe kok tong siantar',
                    'item_url': 'https://majalah.ottencoffee.co.id/mencerup-sejarah-di-cafe-kok-tong-siantar/',
                    'image_url': 'https://majalah.ottencoffee.co.id/wp-content/uploads/2016/12/kedai-kopi-kok-tong-siantar.jpg',
                    'buttons': [{
                      'type': 'web_url',
                      'url': "https://majalah.ottencoffee.co.id/mencerup-sejarah-di-cafe-kok-tong-siantar/",
                      'title': "Selengkapnya"
                    }],
                  }]
                }
              }
            page.send(sender_id, postback)
            return

        if 'MOCHACCINO_PAYLOAD' in payload:
            postback = {
                'type': 'template',
                'payload': {
                  'template_type': 'generic',
                  'elements': [{
                    'title': 'Mocha Coffee',
                    'subtitle': 'Lebih suka espresso atau filter',
                    'item_url': 'https://majalah.ottencoffee.co.id/kamu-lebih-suka-espresso-atau-filter-coffee/',
                    'image_url': 'https://majalah.ottencoffee.co.id/wp-content/uploads/2017/07/public-espresso-yeahbuffalo-007.jpg',
                    'buttons': [{
                      'type': 'web_url',
                      'url': "https://majalah.ottencoffee.co.id/kamu-lebih-suka-espresso-atau-filter-coffee/",
                      'title': "Selengkapnya"
                    }],
                  }]
                }
              }
            page.send(sender_id, postback)
            return

    coffee_menu(payload)
    page.send(sender_id, "Postback called")
