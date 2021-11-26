

class Future:
    """Generic Future interface"""

    def get(self, timeout=None):
        """Retrieve the result"""
        raise NotImplementedError()

    def wait(self, timeout=None):
        """Wait for the underlying job to finish"""
        raise NotImplementedError()

    def ready(self):
        """Returns true if the underlying job has finished"""
        raise NotImplementedError()

    def successful(self):
        """Returns true if the underlying job did not raise an exception"""
        raise NotImplementedError()


class FutureArray:
    """Arrays of Futures"""

    def __init__(self, futures, ordered=False):
        self.futures = futures
        self.ordered = ordered

    def get(self):
        """Wait for all our results and return them"""
        return [f.get() for f in self.futures]

    def __iter__(self):
        return self

    def __next__(self):
        if self.ordered:
            return self.ordered_get()
        return self.unordered_get()
        
    def ordered_get(self):
        """wait for the first future to be ready"""
        if not self.futures:
            raise StopIteration()

        f = self.futures.pop(0)
        return f.get()

    def unordered_get(self):
        """Get the first future that is ready"""
        if not self.futures:
            raise StopIteration()

        selected = None

        while True:
            self.futures[0].wait(0.01)

            for future in self.futures:
                if future.ready():
                    selected = future
                    break

        self.futures.remove(selected)
        return selected.get()



class Executor:
    """Simple executor interface"""

    def __init__(self, n_workers):
        pass

    def __del__(self):
        self.shutdown()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()

    def submit(self, fn, /, *args, **kwargs) -> FutureArray:
        pass

    def map(self, func, *iterables, timeout=None, chunksize=1):
        pass

    def shutdown(self, wait=True, *, cancel_futures=False):
        pass


class Pool:
    """Basic Pool interface"""

    def __init__(self, n_workers):
        self.n_workers = n_workers

    def __del__(self):
        self.terminate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.terminate()

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
        raise NotImplementedError()

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

    def map_async(self, func, iterable) -> FutureArray:
        """

        Examples
        --------
 
        >>> from apool.testing import inc
        >>> with ThreadPool(5) as p:
        ...     future = p.map_async(inc, (1, 2, 3, 4)) 
        ...     future.get()
        [2, 3, 4, 5]
        
        """
        return FutureArray([self.apply_async(func, (arg,)) for arg in iterable])

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

    def imap_unordered(self, func, iterable):
        """

        Examples
        --------

        >>> from apool.testing import inc
        >>> with ThreadPool(5) as p:
        ...     iter = p.imap(inc, (1, 2, 3, 4)) 
        ...     sorted(list(iter))
        [2, 3, 4, 5]

        """
        raise FutureArray([self.apply_async(func, (arg,)) for arg in iterable], False)

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

    def starmap_async(self, func, iterable) -> FutureArray:
        """

        Examples
        --------

        >>> from apool.testing import add
        >>> with ThreadPool(5) as p:
        ...     future = p.starmap_async(add, [(1, 2), (4, 5)]) 
        ...     future.get()
        [3, 9]
        
        """
        return FutureArray([self.apply_async(func, args) for args in iterable])

    def close(self):
        """Prevent new work from being inserted"""
        pass

    def terminate(self):
        """Close the pool and join"""
        pass

    def join(self):
        """wait for all the workers to finish, need to call close first"""
        pass
