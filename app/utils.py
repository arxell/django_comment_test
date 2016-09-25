import logging
import time


log = logging.getLogger(__name__)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        log.debug('{method} {time} (sec)'.format(
            method=method.__name__,
            time=te - ts)
        )
        return result

    return timed


def query_get_one(query):
    """
    x100 faster than

    <model>.objects.filter(...).first()

    return object instance or None
    """
    objects = query.all()[:1]
    if objects:
        return objects[0]
