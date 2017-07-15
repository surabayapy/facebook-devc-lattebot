# -*- coding: utf-8 -*-
"""
    Application Startup
    ~~~~~~~~~
    
    :copyright: (c) 2017 by Nanang Suryadi.
    :license: BSD, see LICENSE for more details.
    
    app.py
"""
from baka import Baka, log

app = Baka(__name__)


@app.route('/')
def index(_):

    return {'LatteBot': 'Surabaya.py dan Facebook DevC Surabaya'}


@app.route('/chat')
def validate(_):
    if _.params.get('hub.mode', '') == 'subscribe' and \
                    _.params.get('hub.verify_token', '') == app.config.settings['VERIFY_TOKEN']:

        print("Validating webhook")

        return _.params.get('hub.challenge', '')
    else:
        return 'Failed validation. Make sure the validation tokens match.'


@app.route('/chat', request_method='POST')
def webhook(_):

    return {'latte': 'post webhook'}

app.scan()
