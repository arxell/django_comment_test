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
