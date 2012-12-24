import pickle
import random
from google.appengine.api import memcache

MEMCACHE_MAX_ITEM_SIZE = 900 * 1024

def delete(key):
    chunk_keys = memcache.get(key)
    if chunk_keys is None:
        return False
    chunk_keys.append(key)
    memcache.delete_multi(chunk_keys)
    return True

def set(key, value, namespace="blobcache", time=86400):
    pickled_value = pickle.dumps(value)
    
    # delete previous entity with the given key
    # in order to conserve available memcache space.
    delete(key)

    pickled_value_size = len(pickled_value)
    chunk_keys = []
    for pos in range(0, pickled_value_size, MEMCACHE_MAX_ITEM_SIZE):
        # TODO: use memcache.set_multi() for speedup, but don't forget
        # about batch operation size limit (32Mb currently).
        chunk = pickled_value[pos:pos + MEMCACHE_MAX_ITEM_SIZE]
        
        # the pos is used for reliable distinction between chunk keys.
        # the random suffix is used as a counter-measure for distinction
        # between different values, which can be simultaneously written
        # under the same key.
        chunk_key = '%s%d%d' % (key, pos, random.getrandbits(31))
        
        is_success = memcache.set(chunk_key, chunk, namespace=namespace, time=time)
        if not is_success:
            return False
        chunk_keys.append(chunk_key)
    return memcache.set(key, chunk_keys, namespace=namespace, time=time)

def get(key, namespace="blobcache"):
    chunk_keys = memcache.get(key, namespace=namespace)
    if chunk_keys is None:
        return None
    chunks = []
    for chunk_key in chunk_keys:
        # TODO: use memcache.get_multi() for speedup.
        # Don't forget about the batch operation size limit (currently 32Mb).
        chunk = memcache.get(chunk_key, namespace=namespace)
        if chunk is None:
            return None
        chunks.append(chunk)
    pickled_value = ''.join(chunks)
    try:
        return pickle.loads(pickled_value)
    except Exception:
        return None

