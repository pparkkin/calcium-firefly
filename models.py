
from google.appengine.ext import ndb

class Item(ndb.Model):
    description = ndb.TextProperty()
    owner = ndb.StringProperty()
    swap = ndb.KeyProperty(kind='Swap', default=None)

    def get_id(self):
        k = self.key
        return k.id()

class Swap(ndb.Model):
    one = ndb.KeyProperty(kind='Item')
    two = ndb.KeyProperty(kind='Item')
