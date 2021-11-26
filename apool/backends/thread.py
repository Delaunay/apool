from concurrent.futures import ThreadPoolExecutor, TimeoutError, wait

from apool.interfaces import Future, Pool


class _ThreadFuture(Future):
    """Wraps a concurrent Future to behave like AsyncResult
    
    Examples
    --------

    >>> from apool import Pool, Thread
    >>> from apool.testing import fun

    >>> with Pool(Thread, 5) as p:
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


class ThreadExecutor(Executor):
    
    def __init__(self, n_workers):
        self.exec = ThreadPoolExecutor(n_workers)

    def submit(self, fn, *args, **kwargs):
        """

        Examples
        --------

        >>> from apool import Executor, Thread
        >>> from apool.testing import fun

        >>> with Executor(Thread, 5) as p:
        ...     future = p.submit(fun, 1, 2, c=3, d=4) 
        ...     future.get()
        10
        
        """
        return _ThreadFuture(self.exec.submit(fn, *args, **kwargs))

    def map(self, func, *iterables, timeout=None, chunksize=1):
        """

        Examples
        --------

        >>> from apool import Executor, Thread
        >>> from apool.testing import inc

        >>> with Executor(Thread, 5) as p:
        ...     iter = p.imap(inc, 1, 2, 3, 4) 
        ...     list(iter)
        [2, 3, 4, 5]
        
        """
        return self.exec.map(func, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait=True, *, cancel_futures=False):
        return self.exec.shutdown(wait=wait, cancel_futures=cancel_futures)


class ThreadPool(Pool):
    """Custom pool that creates multiple threads instead of processess"""

    def __init__(self, n_workers):
        self.pool = ThreadPoolExecutor(n_workers)

    def apply_async(self, fun, args, kwds=None) -> Future:
        """

        Examples
        --------

        >>> from apool import Pool, Thread
        >>> from apool.testing import fun

        >>> with Pool(Thread, 5) as p:
        ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        if kwds is None:
            kwds = dict()
        
        return _ThreadFuture(self.pool.submit(fun, *args, **kwds))

    def close(self):
        self.pool.shutdown()

    def terminate(self):
        self.pool.shutdown()

    def join(self):
        self.pool.shutdown()
