
import json
import webapp2

from authentication import with_email
from models import Item, Swap

def get_email(token):
    return "test.example@email.com"

class SwapsEndpoint(webapp2.RequestHandler):
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
        o = r.get("my_item", None)
        t = r.get("other_item", None)
        if o is None or t is None:
            self.response.status = 400
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Request missing item field"}))
            return
        one = Item.get_by_id(int(o))
        two = Item.get_by_id(int(t))
        if one is None or two is None:
            self.response.status = 500
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Unable to find item"}))
            return
        if one.owner != e:
            self.response.status = 403 # not really with the spec, but lets just go with this for now
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "The item you are trying to swap is not yours"}))
            return
        s = Swap(one=one.key, two=two.key)
        k = s.put()
        one.swap = k
        two.swap = k
        one.put()
        two.put()
        self.response.status = 200
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            "id": str(k.id())
        }))
