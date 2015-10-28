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
  >> features = np.random.randint(0, 10, (120, 4))  # 120 items, 4 dimensionnal features
  >> classes = np.array(np.random.randint(0, 4, (120,)), dtype='S1')  # 3 classes
  >> from abx_numpy import abx
  >> abx(classes, features, lambda x, y: np.linalg.norm(x-y))


Example
-------

See 2D_normal_example.py in 'example/'.

.. image:: examples/data.png
    :width: 10%

Average abx score: 0.82

===== ==== ==== ====
class  1    2    3
===== ==== ==== ====
 1    N/A  0.76 0.85
 2    0.64 N/A  0.74
 3    0.96 0.95 N/A
===== ==== ==== ====

Documentation
-------------

Complete documentation can be found `here <http://abx-numpy.readthedocs.org/en/latest/>`_.
