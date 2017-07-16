# -*- coding: utf-8 -*-
"""
    Event Parsing Payload
    ~~~~~~~~~

    :author: nanang.jobs@gmail.com
    :copyright: (c) 2017 by Nanang Suryadi.
    :license: BSD, see LICENSE for more details.
    
    event.py
"""


class Event(object):
    """Objek Event digunakan untuk mengektrasi data payload"""

    def __init__(self, messaging=None):
        if messaging is None:
            messaging = {}

        self.messaging = messaging
        self.matched_callbacks = []

    @property
    def sender_id(self):
        """ID Pengirim attribute"""
        return self.messaging.get("sender", {}).get("id", None)

    @property
    def recipient_id(self):
        """ID Penerima attribute"""
        return self.messaging.get("recipient", {}).get("id", None)

    @property
    def timestamp(self):
        """timestamp attribute"""
        return self.messaging.get("timestamp", None)

    @property
    def message(self):
        """Pesan attribute"""
        return self.messaging.get("message", {})

    @property
    def message_text(self):
        """Text attribute"""
        return self.message.get("text", None)

    @property
    def message_attachments(self):
        """Attachments attribute"""
        return self.message.get("attachments", [])

    @property
    def postback(self):
        """Postback attribute"""
        return self.messaging.get("postback", {})

    @property
    def message_mid(self):
        """Message.Mid attribute"""
        return self.messaging.get("message", {}).get("mid", None)

    @property
    def postback_payload(self):
        return self.messaging.get("postback", {}).get("payload", '')

    @property
    def is_message(self):
        return 'message' in self.messaging

    @property
    def is_postback(self):
        return 'postback' in self.messaging

    @property
    def is_text_message(self):
        return self.messaging.get("message", {}).get("text", None) is not None

    @property
    def is_attachment_message(self):
        return self.messaging.get("message", {}).get("attachments", None) is not None

    @property
    def is_quick_reply(self):
        return self.messaging.get("message", {}).get("quick_reply", None) is not None

    @property
    def is_echo(self):
        return self.messaging.get("message", {}).get("is_echo", None) is not None
