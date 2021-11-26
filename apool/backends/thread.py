from concurrent.futures import ThreadPoolExecutor, TimeoutError, wait

from apool.interfaces import Future, Pool


class _ThreadFuture(Future):
    """Wraps a concurrent Future to behave like AsyncResult
    
    Examples
    --------

    >>> from apool.testing import fun
    >>> with ThreadPool(5) as p:
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


class _MultiFuture:
    def __init__(self, futures):
        self.futures = futures

    def get(self):
        return [f.get() for f in self.futures]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.futures:
            raise StopIteration()
            
        f = self.futures.pop(0)
        return f.get()


class ThreadPool(Pool):
    """Custom pool that creates multiple threads instead of processess"""

    def __init__(self, n_workers):
        self.pool = ThreadPoolExecutor(n_workers)

    def apply(self, fun, args, kwds=None):
        """

        Examples
        --------

        >>> from apool.testing import fun
        >>> with ThreadPool(5) as p:
        ...     p.apply(fun, (1, 2), dict(c=3, d=4)) 
        10
        
        """
        return self.apply_async(fun, args, kwds).get()

    def apply_async(self, fun, args, kwds=None) -> Future:
        """

        Examples
        --------

        >>> from apool.testing import fun
        >>> with ThreadPool(5) as p:
        ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        if kwds is None:
            kwds = dict()
        
        return _ThreadFuture(self.pool.submit(fun, *args, **kwds))

    def map(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import inc
        >>> with ThreadPool(5) as p:
        ...     p.map(inc, (1, 2, 3, 4)) 
        [2, 3, 4, 5]
        
        """
        return [self.apply(func, (arg,)) for arg in iterable]

    def map_async(self, func, iterable):
        """

        Examples
        --------
 
        >>> from apool.testing import inc
        >>> with ThreadPool(5) as p:
        ...     future = p.map_async(inc, (1, 2, 3, 4)) 
        ...     future.get()
        [2, 3, 4, 5]
        
        """
        return _MultiFuture([self.apply_async(func, (arg,)) for arg in iterable])

    def imap(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import inc
        >>> with ThreadPool(5) as p:
        ...     iter = p.imap(inc, (1, 2, 3, 4)) 
        ...     list(iter)
        [2, 3, 4, 5]

        """
        return self.map_async(func, iterable)

    def starmap(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import add
        >>> with ThreadPool(5) as p:
        ...     p.starmap(add, [(1, 2), (4, 5)]) 
        [3, 9]
        
        """
        return [self.apply(func, args) for args in iterable]

    def starmap_async(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import add
        >>> with ThreadPool(5) as p:
        ...     future = p.starmap_async(add, [(1, 2), (4, 5)]) 
        ...     future.get()
        [3, 9]
        
        """
        return _MultiFuture([self.apply_async(func, args) for args in iterable])

    def close(self):
        self.pool.shutdown()

    def terminate(self):
        self.pool.shutdown()

    def join(self):
        self.pool.shutdown()
