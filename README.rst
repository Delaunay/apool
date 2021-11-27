apool
=====

    One API to find them, One API to bring them, One API to rule them all

Harmonize different concurrency and parallelism API into a single one.

Python standard libaries implements Pool, Executors, each of them with a slightly different
API and with their respective Futures. This library brings them together.


.. code-block:: bash

   pip install apool


.. image:: https://codecov.io/gh/Delaunay/apool/branch/main/graph/badge.svg?token=gQo0w4KQBV
   :target: https://codecov.io/gh/Delaunay/apool


.. image:: https://readthedocs.org/projects/apool/badge/?version=latest
   :target: https://apool.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Features
--------

* Backends

  * Dask
  * Multiprocess (standard python)
  * Threading (standard python)


Examples
--------

Pool API
~~~~~~~~

.. code-block:: python

   from apool import Pool, Dask

   with Pool(Dask, 5) as p:
       future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 

       future.wait()

       result = future.get()


Executor API
~~~~~~~~~~~~

.. code-block:: python

   from apool import Executor, Dask

   with Executor(Dask, 5) as p:
       future = p.submit(fun, 1, 2, c=3, d=4)

       future.wait()

       result = future.get()
