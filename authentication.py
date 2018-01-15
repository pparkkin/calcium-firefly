import httplib2
import json
import logging
import random
import webapp2

from apiclient.discovery import build
from google.appengine.ext import ndb
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials

import os
host = os.environ['HTTP_HOST']

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = flow_from_clientsecrets(
    'client_secret.json',
    scope = ['profile', 'https://www.googleapis.com/auth/userinfo.email'],
    redirect_uri = 'http://{}/oauth2callback'.format(host))

def with_email(f):
    def w(self):
        token = self.request.headers.get("X-Auth-Token", None)
        logging.info("Got token {}".format(token))
        credentials = retrieve_credentials(token)
        email = get_email(credentials)
        return f(self, email)
    return w

def get_email(credentials):
    if credentials is None: return None
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('people', 'v1', http=http)
    req = service.people().get(
        resourceName = 'people/me',
        personFields = 'emailAddresses')
    res = req.execute(http=http)
    logging.info("Service response {}".format(res))
    es = res.get("emailAddresses")
    if es is None or len(es) < 1:
        return "No email address found"
    return es[0]["value"]

def generate_token(credentials):
    random.SystemRandom()
    length=12
    allowed_chars=('abcdefghijklmnopqrstuvwxyz'
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return ''.join(random.choice(allowed_chars) for i in range(length))

class Credentials(ndb.Model):
    token = ndb.StringProperty()
    credentials = ndb.TextProperty()

def store_credentials(token, credentials):
    # I'm just gonna store them for now. Probably should have some way of
    # expiring them, but that can wait.
    if credentials is None: return

    logging.debug("Storing credentials for token '{}'".format(token))
    c = Credentials(token=token, credentials=credentials.to_json())

    c.put()

def retrieve_credentials(token):
    if token is None or token == '': return None

    logging.debug("Retrieving credentials for token '{}'".format(token))

    c = Credentials.query(Credentials.token == token).get()
    if c is None: return None

    return OAuth2Credentials.from_json(c.credentials)

class AuthEndpoint(webapp2.RequestHandler):
    def post(self):
        logging.info("AuthEndpoint arguments: {}".format(self.request.arguments()))
        self.response.headers['Content-Type'] = 'application/json'
        res = {
            'oauth_url': flow.step1_get_authorize_url()
        }
        self.response.write(json.dumps(res))

class Oauth2Callback(webapp2.RequestHandler):
    def get(self):
        logging.info("Oauth2Callback arguments: {}".format(self.request.arguments()))
        code = self.request.get("code")
        credentials = flow.step2_exchange(code)
        logging.info(credentials.to_json())
        email = get_email(credentials)
        token = generate_token(credentials)
        store_credentials(token, credentials)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(token)
