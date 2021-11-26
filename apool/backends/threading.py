from concurrent.futures import ThreadPoolExecutor, TimeoutError, wait

from apool.interfaces import Future, Pool


class _ThreadFuture(Future):
    """Wraps a concurrent Future to behave like AsyncResult
    
    Examples
    --------

    >>> with ThreadPool(5):
    ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4))
    ...     # wait for the future to finish
    ...     future.wait()
    ...     # check if the job has finished
    ...     future.ready()
    True
    ...     # check if the job raised an exception or not
    ...     future.succesful()
    True
    ...     # retrieve the result
    ...     future.get()
    10

    """

    def __init__(self, future):
        self.future = future

    def get(self, timeout=None):
        return self.future.result(timeout)

    def wait(self, timeout=None):
        wait([self.future], timeout)

    def ready(self):
        return self.future.done()

    def successful(self):
        if not self.future.done():
            raise ValueError()

        return self.future.exception() is None


class ThreadPool(Pool):
    """Custom pool that creates multiple threads instead of processess"""

    def __init__(self, n_workers):
        self.pool = ThreadPoolExecutor(n_workers)

    def apply(self, fun, args, kwds=None):
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.apply(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.apply_async(fun, args, kwds).get()

    def apply_async(self, fun, args, kwds=None) -> Future:
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        raise NotImplementedError()

    def map(self, func, iterable):
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.map(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.map_async(func, iterable).get()

    def map_async(self, func, iterable):
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.map_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        raise NotImplementedError()

    def imap(self, func, iterable):
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.imap(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.imap_async(func, iterable).get()

    def imap_async(self, func, iterable):
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.imap_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        raise NotImplementedError()

    def starmap(self, func, iterable):
        return self.starmap_async(func, iterable).get()
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.starmap(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """

    def starmap_async(self, func, iterable):
        """

        Examples
        --------

        >>> with ThreadPool(5) as p:
        ...     future = p.starmap_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        raise NotImplementedError()

    def close(self):
        pass

    def terminate(self):
        pass

    def join(self):
        pass
