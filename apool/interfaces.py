

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
        return self.apply_async(fun, args, kwds).get()

    def apply_async(self, fun, args, kwds=None) -> Future:
        raise NotImplementedError()

    def map(self, func, iterable):
        return self.map_async(func, iterable).get()

    def map_async(self, func, iterable):
        raise NotImplementedError()

    def imap(self, func, iterable):
        return self.imap_async(func, iterable).get()

    def imap_async(self, func, iterable):
        raise NotImplementedError()

    def starmap(self, func, iterable):
        return self.starmap_async(func, iterable).get()

    def starmap_async(self, func, iterable):
        raise NotImplementedError()

    def close(self):
        """Prevent new work from being inserted"""
        pass

    def terminate(self):
        """Close the pool and join"""
        pass

    def join(self):
        """wait for all the workers to finish, need to call close first"""
        pass
