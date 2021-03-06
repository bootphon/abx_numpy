# -*- coding: utf-8 -*-
"""
abx_numpy: Main module

Copyright 2015, Roland Thiolliere
Licensed under GPLv3.
"""
import numpy as np
import itertools
from . import lib


def score(classes, distances, is_sorted=False):
    """Compute the ABX score for a set of sorted classes and a distance matrix.

    Parameters:
    -----------
    classes : array (n_items)
        1-D array containing the sorted class labels of the items.
    distances : array (n_items, n_items)
        2-D array containing the pairwise distance of the items.

    Returns
    -------
    average : float
        average abx score
    labels : array (n_classes)
        1D array containing the unique classes
    scores : array (n_classes, n_classes)
        2D array containing the abx scores for each pair of classes.
        The diagonal contains nan values
    """
    if not is_sorted:
        order = np.argsort(classes)
        _classes, _distances = classes[order], distances[order, :][:, order]
    else:
        _classes, _distances = classes, distances
    labels, indexes = lib.unique_sorted(_classes)
    
    class Index(object):
        def __init__(self, indexes):
            self.indexes_first = indexes[:-1]
            self.indexes_last = indexes[1:]
        def get_slice(self, idx):
            return slice(self.indexes_first[idx], self.indexes_last[idx], 1)

    index = Index(indexes)        
    n_labels = len(labels)
    # scores = np.empty((n_labels, n_labels))
    scores = np.zeros((n_labels, n_labels))
    scores[np.diag_indices(n_labels)] = np.nan
    for idx_label1, idx_label2 in itertools.product(range(n_labels), range(n_labels)):
        if idx_label1 == idx_label2:
            continue
        else:
            items_a = index.get_slice(idx_label1)
            items_b = index.get_slice(idx_label2)
            for a in range(items_a.start, items_a.stop):
                items_x = list(range(items_a.start, a)) + list(range(a+1, items_a.stop))
                d_ax = np.tile(_distances[a, items_x], (items_b.stop - items_b.start, 1))
                d_bx = _distances[items_b, :][:, items_x]
                scores[idx_label1, idx_label2] += np.mean(np.int8(d_ax < d_bx) - np.int8(d_ax > d_bx))
            scores[idx_label1, idx_label2] = ((scores[idx_label1, idx_label2] / (items_a.stop - items_a.start)) + 1) * 0.5
    return np.nanmean(scores), labels, scores


def compute_distances(features, distance_function):
    """Compute the distance matrix for an array of features and a distance
    function.

    Parameters
    ----------
    features : array (n_items, dim_features)
        2-D array containing the features of the items.
    distance_function : callable
        Distance function to use.

    Returns
    -------
    distances : array (n_items, n_items)
        2-D array containing the pairwise distance of the items.
    """
    n_items = features.shape[0]
    distances = np.empty((n_items, n_items))
    #TODO: cython, only lower triangle in symmetric distance
    for i, j in itertools.product(range(n_items), range(n_items)):
        distances[i, j] = distance_function(features[i], features[j])
    return distances


def sort(classes, features):
    """Sort classes according to labels and features according to the new order"""
    order = np.argsort(classes)
    return classes[order], features[order]


def sample(classes, features, cutoff, is_sorted=False):
    """'Fair' sampling (non-uniform, inverse to the class weight)

    Parameters
    ----------
    classes : array (n_items)
        1-D array containing the class labels of the items.
    features : array (n_items, dim_features)
        2-D array containing the features of the items.
    cutoff : int
        Cutoff to use for sample (number of items kept).

    Returns
    -------
    sampled classes, sampled features
    """
    #TODO: improve fairness by enforcing the number of element in each class
    # to be equal
    if not is_sorted:
        _classes, _features = sort(classes, features)
    else:
        _classes, _features = classes, features
    n_items = _classes.shape[0]
    labels, indexes = lib.unique_sorted(_classes)
    size_classes = indexes[1:] - indexes[:-1]
    proba_sampling = np.repeat(1. / (size_classes * len(labels)), size_classes)
    indexes = np.random.choice(n_items, size=cutoff, replace=False, p=proba_sampling)
    indexes = np.sort(indexes)
    return _classes[indexes], _features[indexes]


def abx(classes, features, distance_function, cutoff=1000):
    """Calculate the ABX score for a set of classes and a features matrix.

    The order of the 'classes' and the 'features' arrays must be the same.

    Parameters
    ----------
    classes : array (n_items)
        1-D array containing the class labels of the items.
    features : array (n_items, dim_features)
        2-D array containing the features of the items.
    distance_function : callable
        Distance function to use.
    cutoff : int, optionnal
        Cutoff to use for sample (number of items kept). None for no sample.
        Default to 1000.

    Returns
    -------
    average : float
        average abx score
    labels : array (n_classes)
        1D array containing the unique classes
    scores : array (n_classes, n_classes)
        2D array containing the abx scores for each pair of classes.
        The diagonal contains nan values
    """
    assert classes.shape[0] == features.shape[0]
    _classes, _features = sort(classes, features)
    if cutoff and cutoff < _classes.shape[0]:
        _classes, _features = sample(_classes, _features, cutoff, is_sorted=True)
    distances = compute_distances(_features, distance_function)
    average, labels, scores = score(_classes, distances, is_sorted=True)
    return average, labels, scores



# def score2(classes, distances):
#     raise NotImplementedError
#             a = index.get_slice(idx_label1)
#             b = index.get_slice(idx_label2)
#             n_a = a.stop - a.start
#             x = np.eye(n_a, dtype=bool)
#             d_ax = _distances[a, a][~x].reshape((n_a, n_a-1)).T[None, :, :]
#             d_bx = _distances[b, a][:, None, :]
#             scores[idx_label1, idx_label2] = (np.mean((d_ax < d_bx) - (d_ax > d_bx))) * 0.5
