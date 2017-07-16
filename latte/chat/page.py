# -*- coding: utf-8 -*-
"""
    Page Messenger
    ~~~~~~~~~

    :author: nanang.jobs@gmail.com
    :copyright: (c) 2017 by Nanang Suryadi.
    :license: BSD, see LICENSE for more details.
    
    page.py
"""
from collections import OrderedDict
import json
import sys
from baka import log
from .event import Event
from ..util import Api, to_json

HEADERS = {'Content-type': 'application/json'}
OK = 200


class Page(object):

    def __init__(self, access_token, **options):
        self.access_token = access_token
        self._page_id = None
        self._page_name = None

    @property
    def page_id(self):
        if self._page_id is None:
            self._fetch_page_info()

        return self._page_id

    @property
    def page_name(self):
        if self._page_name is None:
            self._fetch_page_info()

        return self._page_name

    def _fetch_page_info(self):
        r = Api.get('https://graph.facebook.com/v2.6/me',
                    params={'access_token': self.access_token},
                    headers=HEADERS)

        if r.status_code != OK:
            log.error(r.text)
            return

        data = json.loads(r.text)
        if 'id' not in data or 'name' not in data:
            raise ValueError('Could not fetch data : GET /v2.6/me')

        self._page_id = data['id']
        self._page_name = data['name']

    def get_user_profile(self, fb_user_id):
        r = Api.get('https://graph.facebook.com/v2.6/%s' % fb_user_id,
                    params={'access_token': self.access_token},
                    headers=HEADERS)

        if r.status_code != OK:
            log.error(r.text)
            return

        return json.loads(r.text)

    """
    messenger_profile settings
    """
    def _send_profile_settings(self, data, method='post'):
        r = Api.route(method, 'https://graph.facebook.com/v2.6/me/messenger_profile',
                      params={'access_token': self.access_token},
                      data=data,
                      headers=HEADERS)

        if r.status_code != OK:
            log.error(r.text)

    def greeting(self, text):
        if not text or not isinstance(text, str):
            raise ValueError('greeting text pesan harus string')

        self._send_profile_settings(json.dumps({
            'greeting': [{
                'locale': 'default',
                'text': text
            }]
        }))

    def show_starting_button(self, payload):
        if not payload or not isinstance(payload, str):
            raise ValueError('show_starting_button payload harus string')

        self._send_profile_settings(json.dumps({
            'get_started': [
                {
                    'payload': payload
                }
            ]
        }))

    def hide_starting_button(self):
        self._send_profile_settings(json.dumps({
            "fields": [
                "get_started"
            ]
        }), 'delete')

    def show_persistent_menu(self, buttons):
        if type(buttons) == OrderedDict:
            buttons = [buttons]

        self._send_profile_settings(json.dumps({
            "locale": "default",
            "composer_input_disabled": True,
            "call_to_actions": buttons
        }))

    def hide_persistent_menu(self):
        self._send_profile_settings(json.dumps({
            "fields": [
                "persistent_menu"
            ]
        }), 'delete')

    """
    handle webhook messaging
    """

    def send(self, recipient_id, message, callback=None):
        """
            text
            message = {
                'text': 'text message'
            }
            attachment
            message = {
                'attachment': {
                    'type': 'template',
                    'payload': {}
                }
            }
        """
        if sys.version_info >= (3, 0):
            text = message if isinstance(message, str) else None
        else:
            text = message if isinstance(message, str) else \
                message.encode('utf-8') if isinstance(message, unicode) else None

        attachment = message if not text else None

        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': text
        }

        return self._send(payload, callback=callback)

    def _send(self, payload, callback=None):
        assert type(payload) == dict, 'tipe payload harus dict'

        if type(payload) == object:
            payload = to_json(payload)

        log.info(payload)
        """
        r = Api.post('https://graph.facebook.com/v2.6/me/messages',
                     params={'access_token': self.access_token},
                     data=payload,
                     headers=HEADERS)

        if r.status_code != OK:
            log.error(r.text)
            return

        if callback is not None:
            callback(payload, r)

        return json.loads(r.text)
        """

    def handle_webhook(self, payload, message_callback=None, postback_callback=None):

        _data = payload

        if type(payload) is not object and isinstance(payload, str):
            _data = json.loads(payload)

        # Memastikan Page sudah di subscribe
        if _data.get('object') != 'page':
            log.error('Webhook failed, only support page subscription')
            return False

        # men-routing tipe pesan yang datang dari webhook
        def get_events(_data_):
            for entry in _data_.get("entry"):
                for messaging in entry.get("messaging"):
                    event = Event(messaging)
                    yield event

        for event in get_events(_data):
            if event.is_message and not event.is_echo and not event.is_quick_reply:
                if message_callback is None:
                    log.error('message_callback is None')
                    continue
                message_callback(event)

            elif event.is_postback:
                if postback_callback is None:
                    log.error('postback_callback is None')
                    continue
                postback_callback(event)
            else:
                log.error('Webhook received unknown messagingEvent:', event)
