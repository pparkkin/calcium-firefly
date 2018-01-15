
import logging
import webapp2

from authentication import AuthEndpoint, Oauth2Callback, with_email
from items import ItemsEndpoint
from swaps import SwapsEndpoint

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        f = file('README.md', 'r')
        self.response.write(f.read())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/auth', AuthEndpoint),
    ('/oauth2callback', Oauth2Callback),
    ('/items', ItemsEndpoint),
    ('/swaps', SwapsEndpoint),
], debug=True)
