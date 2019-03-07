# -*- coding: utf-8 -*-
import os
import json
import logging

import webapp2

from google.appengine.api import memcache
from google.appengine.api import urlfetch


class ProxyHandler(webapp2.RequestHandler):

  def get(self):
    url = os.environ['ORIGIN_URL']
    result = memcache.get(url)
    if result is None:
      try:
        urlfetch.set_default_fetch_deadline(300)
        response = urlfetch.fetch(url)
        if response.status_code == 200:
          result = response.content
          memcache.set(url, result, time=300)
        else:
          self.response.status_code = response.status_code
      except urlfetch.Error:
        logging.exception('caught exception fetching url')

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(result)


app = webapp2.WSGIApplication([
  ('/', ProxyHandler),
], debug=False)

