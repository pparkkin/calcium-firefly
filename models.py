
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

    def get_id(self):
        k = self.key
        return k.id()

    @classmethod
    # failure probably means the items were added to a different swap, no need to retry
    @ndb.transactional(retries=0, xg=True)
    def create(cls, one, two):
        s = cls(one=one.key, two=two.key)
        k = s.put()
        one.swap = k
        two.swap = k
        one.put()
        two.put()
        return s
