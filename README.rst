apool
=====

One API to find them, One API to bring them, One API to rule them all


Harmonize different concurrency and parallelism API into a single one.


.. code-block:: bash

   pip install apool



Features
--------

* Backends

    * Dask
    * Multiprocess (standard python)
    * Threading (standard python)


Examples
--------

.. code-block:: python

   with Pool(5, backend=dask) as p:
       future = p.apply_async(fun, (1, 2), dict(c=3, d=4)) 

       future.wait()

       result = future.get()
