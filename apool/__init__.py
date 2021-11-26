__descr__ = 'Pool Adapter library for multiprocess and threading'
__version__ = '1.0.0'
__license__ = 'BSD 3-Clause License'
__author__ = u'Pierre Delaunay'
__author_short__ = u'Setepenre'
__author_email__ = 'setepenre@outlook.com'
__copyright__ = u'2021 Pierre Delaunay'
__url__ = 'https://github.com/kiwi-lang/python_seed'


from apool.backends.dask import DaskPool, DaskExecutor
from apool.backends.multiprocess import ProcessPool, ProcessExecutor
from apool.backends.thread import ThreadPool, ThreadExecutor

Process = 0
Thread = 1
Dask = 2



def Pool(cls, *args, **kwargs):
    bks = [ProcessPool, ThreadPool, DaskPool]
    return bks[cls](*args, **kwargs)

def Executor(cls, *args, **kwargs):
    bks = [ProcessExecutor, ThreadExecutor, DaskExecutor]
    return bks[cls](*args, **kwargs)
