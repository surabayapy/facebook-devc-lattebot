# -*- coding: utf-8 -*-
"""
    Util
    ~~~~~~~~~
    
    :author: nanang.jobs@gmail.com
    :copyright: (c) 2017 by Nanang Suryadi.
    :license: BSD, see LICENSE for more details.
    
    util.py
"""
import json
from requests.api import request


class Api:

    def __init__(self):
        self.http = request

    def client(self, method, url, **kwargs):
        return self.http(method, url, **kwargs)

    @classmethod
    def get(cls, url, **kwargs):
        return cls().client('get', url, **kwargs)

    @classmethod
    def post(cls, url, **kwargs):
        """
        default kwargs.setdefault('data', None)
        default kwargs.setdefault('json', None)

        :param url:
        :param kwargs:
        :return:
        """
        return cls().client('post', url, **kwargs)

    @classmethod
    def options(cls, url, **kwargs):
        return cls().client('options', url, **kwargs)

    @classmethod
    def put(cls, url, **kwargs):
        return cls().client('PUT', url, **kwargs)

    @classmethod
    def delete(cls, url, **kwargs):
        return cls().client('DELETE', url, **kwargs)

    @classmethod
    def route(cls, method, url, **kwargs):

        if 'get' in method:
            return cls().get(url, **kwargs)
        if 'post' in method:
            return cls().post(url, **kwargs)
        if 'options' in method:
            return cls().options(url, **kwargs)
        if 'put' in method:
            return cls().put(url, **kwargs)
        if 'delete' in method:
            return cls().delete(url, **kwargs)


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True)
