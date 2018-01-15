
import json
import webapp2

from authentication import with_email
from models import Item, Swap

def get_email(token):
    return "test.example@email.com"

class ItemsEndpoint(webapp2.RequestHandler):
    @with_email
    def post(self, e):
        if e is None:
            self.response.status = 401 # not really with the spec, but lets just go with this for now
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Unable to authenticate"}))
            return
        b = self.request.body
        try:
            r = json.loads(b)
        except Exception:
            self.response.status = 400
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Unable to parse request"}))
            return
        d = r.get("description", None)
        if d is None:
            self.response.status = 400
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Request missing description field"}))
            return
        i = Item(description = d, owner = e)
        k = i.put()
        self.response.status = 200
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            "id": str(k.id())
        }))
    @with_email
    def get(self, e):
        if e is None:
            self.response.status = 401 # not really with the spec, but lets just go with this for now
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Unable to authenticate"}))
            return
        filtered = self.request.get('filter', None)
        q = Item.query().filter(Item.swap == None)
        if filtered == 'own':
            q = q.filter(Item.owner == e)
        elif filtered == 'others':
            q = q.filter(Item.owner != e)
        r = [{"id": str(i.get_id()), "description": i.description, "owner": i.owner} for i in q]
        self.response.status = 200
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(r))
