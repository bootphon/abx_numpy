"""Test suite for abx_numpy
@author: Roland Thiolliere
"""
import numpy as np
import abx_numpy


def generate_items():
    dim = 10
    n_items = 100
    data = np.random.randint(0, 100, (n_items, dim))
    classes = np.random.randint(0, 5, (n_items,))
    return classes, data


def distance_function_test(a, b):
    return np.linalg.norm(a-b)


def test_distances():
    classes, data = generate_items()
    distances = abx_numpy.compute_distances(data, distance_function_test)
    distances


def test_score():
    classes, data = generate_items()
    distances = abx_numpy.compute_distances(data, distance_function_test)
    average, labels, scores = abx_numpy.score(classes, distances)
    

def test_abx():
    classes, data = generate_items()
    abx_score = abx_numpy.abx(classes, data, lambda a, b: np.linalg.norm(a-b))
    abx_score


test_abx()
