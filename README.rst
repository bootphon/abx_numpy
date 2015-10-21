==================================================================
abx_numpy: Small ABX evaluation
==================================================================

.. image:: https://travis-ci.org/bootphon/abx_numpy.svg?branch=master
    :target: https://travis-ci.org/bootphon/abx_numpy

This package is a simpler version of the ABXpy package, for smaller task wth less constraints.

Input and output format are easier to use.

Installation
------------

::

   $ python setup.py build && python setup.py install

Usage
-----

To do an ABX evaluation::

  >> import numpy as np
  >> features = np.random.randint(0, 10, (12, 4))  # 12 items, 4 dimensionnal features
  >> classes = np.random.randint(0, 4, (12,))  # 3 classes
  >> from abx_numpy import abx
  >> abx(classes, features, lambda x, y: np.linalg.norm(x-y))

..
   TODO: This is a good place to start with a couple of concrete examples of how the package should be used.

   The boilerplate code provides a dummy ``main`` function that prints out the word 'Hello'::

       >> from abx_numpy import main
       >> main()

   When the package is installed via ``easy_install`` or ``pip`` this function will be bound to the ``abx_numpy`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).
