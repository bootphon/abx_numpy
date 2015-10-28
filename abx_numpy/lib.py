# -*- coding: utf-8 -*-
"""
@author: Roland Thiolliere
"""
import numpy as np


def unique_sorted(array):
    """Performs unique on a sorted array and return the unique elements and
    the indexes of the first element of each block.
    """
    n_elements = len(array)
    n_uniques = 1
    indexes = np.empty((n_elements,), dtype=np.int)
    indexes[0] = 0
    uniques = np.empty((n_elements,), dtype=array.dtype)
    uniques[0] = array[0]
    for index, element in enumerate(array[1:]):
        if element != uniques[n_uniques-1]:
            indexes[n_uniques] = index + 1
            uniques[n_uniques] = element
            n_uniques += 1
    indexes[n_uniques] = n_elements
    return uniques[:n_uniques], indexes[:n_uniques+1]
