"""This module contains several distances to use"""
import numpy as np
import scipy as sp


def euclidian(x, y):
    """Eculidian distance"""
    return np.linalg.norm(x - y)


def cosine(x, y):
    """Cosine distance (1 - cosine similaity)"""
    return 1 - (np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))


def kl_divergence(x, y, base=None):
    """Kullback-Leiber divergence"""
    return sp.stats.entropy(x, y, base=base)


def symmetric_kl_divergence(x, y, base=None):
    """Symmetric Kullback-Leiber divergence"""
    return (kl_divergence(x, y) + kl_divergence(y, x)) * 0.5


def js_divergence(x, y, base=None):
    """Jensen-Shannon divergence"""
    return (kl_divergence(x, x + y) + kl_divergence(y, x + y)) * 0.5


def discrete(x, y):
    """Discrete distance (1 if x = y, 0 otherwise"""
    return np.all(x == y)


def hamming(x, y):
    """Hamming distance"""
    return np.sum(x == y)
