# -*- coding: utf-8 -*-
"""
abx_numpy: Main module

Copyright 2015, Roland Thiolliere
Licensed under GPLv3.
"""
import numpy as np
import itertools
# import abx_numpy.lib as lib
import lib


def score(classes, distances):
    """Compute the ABX score for a set of classes and a distance matrix.

    Parameters:
    -----------
    classes : array (n_items)
        1-D array containing the class labels of the items.
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
    order = np.argsort(classes)
    _classes = classes[order]
    _distances = distances[order]
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
                items_x = range(items_a.start, a) + range(a+1, items_a.stop)
                d_ax = np.tile(_distances[a, items_x], (items_b.stop - items_b.start, 1))
                d_bx = _distances[items_b, :][:, items_x]
                scores[idx_label1, idx_label2] += (np.mean((d_ax < d_bx) - (d_ax > d_bx))) * 0.5
            scores[idx_label1, idx_label2] /= (items_a.stop - items_a.start)
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


def abx(classes, features, distance_function):
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
    distances = compute_distances(features, distance_function)
    average, labels, scores = score(classes, distances)
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
