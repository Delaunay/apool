import pickle

try:
    import cloudpickle

    HAS_CLOUDPIKLE = None
except ImportError as e:
    HAS_CLOUDPIKLE = e


def _payload(fun, args, kwargs):
    return cloudpickle.dumps((fun, args, kwargs))

def _cloudpickle(payload):
    function, args, kwargs = pickle.loads(payload)
    result = function(*args, **kwargs)
    return cloudpickle.dumps(result)
