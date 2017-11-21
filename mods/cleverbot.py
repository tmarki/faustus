#!/usr/bin/python
""" Cleverbot module """
# -*- coding: utf8 -*-

import requests
import hashlib
import simplejson
import re
import traceback


def decode(raw):
    text = raw
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = raw.decode('iso-8859-1')
        except UnicodeDecodeError:
            text = raw.decode('cp1252')
    return text

class Session(object):
    apikey = ''
    cleversession = ''

    def __init__(self, apikey):
        self.apikey = apikey

    def Send(self, q):
        payload = { "key" : self.apikey, "input" : q, "cs" : self.cleversession }
        r = requests.get("http://www.cleverbot.com/getreply", params=payload)
        reply=r.text
        return reply

    def Ask(self,q):
        q = q.replace(":", " ").strip()
        asw=self.Send(q)
        answer = self.parseAnswers(asw)
        text = answer['output']
        if 'cs' in answer:
                self.cleversession = answer['cs']
        return text

    def parseAnswers(self, text):
        try:
            return simplejson.loads(text)
        except Exception:
            try:
                return simplejson.loads(decode(text).encode('utf8'))
            except Exception:
                print ('Cleverbot wrong json, self recovery')
                self.cleversession = ''
                traceback.print_exc()
        return {'output' : 'Cleverbot problem'}



def main():
    import sys
    cb = Session('replace with cleverbot api key for testing')
    q = ''
    while q != 'bye':
        try:
            q = input("> ")
        except KeyboardInterrupt:
            sys.exit()
        print (cb.Ask(q))

if __name__ == "__main__":
    main()


