"""Test suite for abx_numpy
@author: Roland Thiolliere
"""
import numpy as np
import abx_numpy


tolerance = 0.1


def generate_random_items():
    dim = 10
    n_items = 100
    data = np.random.randint(0, 100, (n_items, dim))
    classes = np.random.randint(0, 5, (n_items,))
    return classes, data


def distance_function_test(a, b):
    return np.linalg.norm(a-b)


def test_random_distances():
    classes, data = generate_random_items()
    distances = abx_numpy.compute_distances(data, distance_function_test)
    distances


def test_random_score():
    classes, data = generate_random_items()
    distances = abx_numpy.compute_distances(data, distance_function_test)
    average, labels, scores = abx_numpy.score(classes, distances)
    assert np.abs(average - 0.5) < tolerance 
    
    
def test_random_abx():
    classes, data = generate_random_items()
    abx_score = abx_numpy.abx(classes, data, lambda a, b: np.linalg.norm(a-b))
    assert np.abs(abx_score[0] - 0.5) < tolerance 


def generate_perfect_items():
    n_classes = 10
    dim = 5
    n_items_per_class = 6
    n_items = n_items_per_class * n_classes
    features = np.repeat(np.arange(n_classes), dim * n_items_per_class)
    features = features.reshape((n_items, dim))
    classes = np.repeat(np.arange(n_classes), n_items_per_class)
    return classes, features


def test_perfect_abx():
    classes, data = generate_perfect_items()
    abx_score = abx_numpy.abx(classes, data, lambda a, b: np.linalg.norm(a-b))
    assert abx_score[0] == 1.
    assert np.all(abx_score[1] == np.arange(10))
    assert np.all(abx_score[2][~np.eye(10, dtype=bool)] == 1)
