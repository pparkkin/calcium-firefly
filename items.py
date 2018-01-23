
import json
import webapp2

from authentication import with_email
from parsing import with_json_body
from models import Item, Swap

class ItemsEndpoint(webapp2.RequestHandler):
    @with_email
    @with_json_body
    def post(self, r, e):
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
