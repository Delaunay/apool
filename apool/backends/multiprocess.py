from multiprocessing import Manager, Process
from multiprocessing.pool import AsyncResult
from multiprocessing.pool import Pool as PyPool

from apool.interfaces import Future, Pool


class _Process(Process):
    """Process that cannot be a daemon"""

    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class _Future:
    """Wraps a python AsyncResult
    
    Examples
    --------

    >>> from apool.testing import fun
    >>> with MultiprocessPool(5) as p:
    ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4))
    
    wait for the future to finish
    
    ...     future.wait()
    
    check if the job has finished
    
    ...     future.ready()
    True
    
    check if the job raised an exception or not
    
    ...     future.succesful()
    True
    
    retrieve the result
    ...     future.get()
    10

    """

    def __init__(self, future, cloudpickle=False):
        self.future = future
        self.cloudpickle = cloudpickle

    def get(self, timeout=None):
        r = self.future.get(timeout)
        return pickle.loads(r) if self.cloudpickle else r

    def wait(self, timeout=None):
        return self.future.wait(timeout)

    def ready(self):
        return self.future.ready()

    def successful(self):
        return self.future.successful()


class _Pool(PyPool):
    """Custom pool that does not set its worker as daemon process"""

    ALLOW_DAEMON = True

    @staticmethod
    def Process(*args, **kwds):
        import sys

        v = sys.version_info

        #  < 3.8 use self._ctx
        # >= 3.8 ctx as an argument
        if v.major == 3 and v.minor >= 8:
            args = args[1:]

        if _Pool.ALLOW_DAEMON:
            return Process(*args, **kwds)

        return _Process(*args, **kwds)


class MultiprocessPool(Pool):
    def __init__(self, n_workers):
        self.pool = _Pool(n_workers)

    def apply(self, fun, args, kwds=None):
        """

        Examples
        --------

        >>> from apool.testing import fun
        >>> with MultiprocessPool(5) as p:
        ...     p.apply(fun, (1, 2), dict(c=3, d=4)) 
        10
        
        """
        return self.pool.apply(fun, args, kwds)

    def apply_async(self, fun, args, kwds=None) -> Future:
        """

        Examples
        --------

        >>> from apool.testing import fun
        >>> with MultiprocessPool(5) as p:
        ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.pool.apply_async(fun, args, kwds)

    def map(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import inc
        >>> with MultiprocessPool(5) as p:
        ...     p.map(inc, (1, 2, 3, 4)) 
        [2, 3, 4, 5]
        
        """
        return self.pool.map(func, iterable)

    def map_async(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import inc
        >>> with MultiprocessPool(5) as p:
        ...     future = p.map_async(inc, (1, 2, 3, 4)) 
        ...     future.get()
        [2, 3, 4, 5]
        
        """
        return self.pool.map_async(func, iterable)

    def imap(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import inc
        >>> with MultiprocessPool(5) as p:
        ...     iter = p.imap(inc, (1, 2, 3, 4)) 
        ...     list(iter)
        [2, 3, 4, 5]
        
        """
        return self.pool.imap(func, iterable)

    def starmap(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import add
        >>> with MultiprocessPool(5) as p:
        ...     p.starmap(add, [(1, 2), (4, 5)]) 
        [3, 9]
        
        """
        return self.pool.starmap(func, iterable)

    def starmap_async(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import add
        >>> with MultiprocessPool(5) as p:
        ...     future = p.starmap_async(add, [(1, 2), (4, 5)]) 
        ...     future.get()
        [3, 9]
        
        """
        return self.pool.starmap_async(func, iterable)

    def close(self):
        self.pool.close()

    def terminate(self):
        self.pool.terminate()

    def join(self):
        self.pool.join()
