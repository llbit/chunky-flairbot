#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Jesper Öqvist <jesper@llbit.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import praw
import re
import requests
import sys
import io
import random, string
import os.path
import json

# To upgrade PRAW: sudo pip install praw --upgrade

try:
    r = praw.Reddit(user_agent='praw:se.llbit.chunky.flairbot:v1.0.3 (by /u/llbit)')
    with open('config.json', 'r') as f:
        config = json.load(f)
        r.set_oauth_app_info(
                client_id=config['client_id'],
                client_secret=config['client_secret'],
                redirect_uri=config['redirect_uri'])
    if os.path.isfile('refresh_token'):
        with open('refresh_token') as f:
            refresh_token = f.readline()
        access_info = r.refresh_access_information(refresh_token)
        r.set_access_credentials(**access_info)

        posts = r.get_subreddit('chunky').get_new(limit=10)

        image = re.compile('^http://((www|i).)?imgur.com/')

        for p in posts:
            if not p.link_flair_text and image.match(p.url):
                print "Setting render flair for \"%s\"" % p.title.encode('utf-8')
                print p.set_flair('render', 'render')
    else:
        # Get new access token for OAuth.
        rand_str = string.join(random.choice(string.lowercase + string.digits) for i in range(10))
        url = r.get_authorize_url(rand_str, 'read modflair', True)
        print url
        code = raw_input("enter access code:")
        access_info = r.get_access_information(code)
        with io.open('refresh_token', 'w', encoding='utf8') as f:
            f.write(access_info['refresh_token'])
except requests.exceptions.HTTPError:
    print "http error"

