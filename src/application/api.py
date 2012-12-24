from eveapi import eveapi
import settings
import blobcache
import logging


def get_api():
    api = eveapi.EVEAPIConnection(cacheHandler=apiMemcacheHandler())
    if len(settings.API_KEYID) > 0 and len(settings.API_VCODE):
        api.auth(keyID=settings.API_KEYID,
                vCode=settings.API_VCODE)
    return api

class apiMemcacheHandler(object):

    def __init__(self):
        self.count = 0
        self.debug = settings.DEBUG

    def log(self, what):
        if self.debug:
            logging.info("[%d] %s", self.count, what)

    def retrieve(self, host, path, params):
        key = "api-%d" % hash((host, path, frozenset(params.items())))

        self.count += 1

        cached = blobcache.get(key, namespace="eveapi")
        if cached is not None:
            self.log("%s in cache" % path)
            return cached

        self.log("%s not cached" % path)
        return None

    def store(self, host, path, params, doc, obj):
        key = "api-%d" % hash((host, path, frozenset(params.items())))

        cachedFor = obj.cachedUntil - obj.currentTime
        self.log("%s added to the cache for %d" % (path, cachedFor))
        blobcache.set(key, doc, namespace="eveapi", time=cachedFor)

