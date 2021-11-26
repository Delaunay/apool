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

    >>> with DaskPool(5):
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


class DaskPool(Pool):
    def __init__(self, n_workers=None):
        if HAS_DASK:
            raise HAS_DASK

        self.config = config
        if client is None:
            client = Client(**self.config)

        self.client = client
    
    def __del__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.terminate()

    def apply(self, fun, args, kwds=None):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     p.apply(fun, (1, 2), dict(c=3, d=4)) 
        10

        """
        return self.apply_async(fun, args, kwds).get()

    def apply_async(self, fun, args, kwds=None) -> Future:
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return _Future(self.client.submit(fun, *args, **kwargs, pure=False))

    def map(self, func, iterable):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     future = p.map(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.map_async(func, iterable).get()

    def map_async(self, func, iterable):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     future = p.map_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        raise NotImplementedError()

    def imap(self, func, iterable):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     future = p.imap(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.imap_async(func, iterable).get()

    def imap_async(self, func, iterable):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     future = p.imap_async(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        raise NotImplementedError()

    def starmap(self, func, iterable):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
        ...     future = p.starmap(fun, (1, 2), dict(c=3, d=4)) 
        ...     future.get()
        10
        
        """
        return self.starmap_async(func, iterable).get()

    def starmap_async(self, func, iterable):
        """

        Examples
        --------

        >>> with Daskpool(5) as p:
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

