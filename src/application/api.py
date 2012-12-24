from eveapi import eveapi
import settings
import blobcache


def get_api():
    if len(settings.API_KEYID) > 0 and len(settings.API_VCODE):
        api = eveapi.EVEAPIConnection(keyID=settings.API_KEY_ID,
                vCode=settings.API_VCODE,
                cacheHandler=apiMemcacheHandler())
    else:
        api = eveapi.EVEAPIConnection(cacheHandler=apiMemcacheHandler())
    return api

class apiMemcacheHandler(object):

    def __init__(self):
        self.count = 0
        self.debug = settings.DEBUG

    def log(self, what):
        if self.debug:
            return
#print "[%d] %s" % (self.count, what)

    def retrieve(self, host, path, params):
        key = "api-%d" % hash((host, path, frozenset(params.items())))

        self.count += 1

        cached = blobcache.get(key, namespace="eveapi")
        if cached is not None:
            self.log("%s in cache" % path)
            return cached

        self.log("%s not cached % path")
        return None

    def store(self, host, path, params, doc, obj):
        key = "api-%d" % hash((host, path, frozenset(params.items())))

        cachedFor = obj.cachedUntil - obj.currentTime
        blobcache.set(key, doc, namespace="eveapi", time=cachedFor)

