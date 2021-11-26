import traceback
from multiprocessing import TimeoutError as PyTimeoutError
from multiprocessing import Value

from apool.interfaces import Future, Pool

try:
    from dask.distributed import (
        Client,
        TimeoutError,
        get_client,
        get_worker,
        rejoin,
        secede,
    )

    HAS_DASK = None
except ImportError as e:
    HAS_DASK = e


class _DaskFuture(Future):
    """Wraps a Dask Future
    
    Examples
    --------

    >>> from apool import Pool, Dask
    >>> from apool.testing import fun

    >>> with Pool(Dask, 5):
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
        
        try:
            return self.future.result(timeout)
        except TimeoutError as e:
            raise PyTimeoutError from e

    def wait(self, timeout=None):
        try:
            self.future.result(timeout)
        except TimeoutError:
            pass

    def ready(self):
        return self.future.done()

    def successful(self):
        if not self.future.done():
            raise ValueError()

        return self.future.exception() is None


class DaskExecutor(Executor):
    
    def __init__(self, n_workers):
        if HAS_DASK:
            raise HAS_DASK

        self.config = config
        if client is None:
            client = Client(**self.config)

        self.client = client

    def submit(self, fn, /, *args, **kwargs):
        """

        Examples
        --------

        >>> from apool import Executor, Dask
        >>> from apool.testing import fun

        >>> with Executor(Dask, 5) as p:
        ...     future = p.submit(fun, 1, 2, c=3, d=4) 
        ...     future.get()
        10
        
        """
        return _DaskFuture(self.client.submit(fn, *args, **kwargs))

    def map(self, func, *iterables, timeout=None, chunksize=1):
        """

        Examples
        --------

        >>> from apool import Executor, Dask
        >>> from apool.testing import inc

        >>> with Executor(Dask, 5) as p:
        ...     iter = p.map(inc, 1, 2, 3, 4) 
        ...     list(iter)
        [2, 3, 4, 5]
        
        """
        return self.client.map(func, *iterables)

    def shutdown(self, wait=True, *, cancel_futures=False):
        return self.client.shutdown(wait=wait, cancel_futures=cancel_futures)


class DaskPool(Pool):
    def __init__(self, n_workers=None):
        if HAS_DASK:
            raise HAS_DASK

        self.config = config
        if client is None:
            client = Client(**self.config)

        self.client = client

    def apply_async(self, fun, args, kwds=None) -> Future:
        """

        Examples
        --------

        >>> from apool import Pool, Dask
        >>> from apool.testing import fun

        >>> with Pool(Dask, 5) as p:
        ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return _DaskFuture(self.client.submit(fun, *args, **kwargs, pure=False))

    def close(self):
        self.client.shutdown()

    def terminate(self):
        self.client.shutdown()

    def join(self):
        self.client.shutdown()

