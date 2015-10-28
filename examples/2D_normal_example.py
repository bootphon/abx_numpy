"""
This example apply the abx evaluation on 2D data sampled from gaussian distributions
"""

import abx_numpy
import numpy as np
import matplotlib.pyplot as plt


def sample_data(parameters):
    data = []
    n_samples = []
    for klass in parameters:
        sample = np.empty((klass['N'], 2))
        for i in range(2):
            sample[:, i] = np.random.normal(klass['mean'][i],
                                            klass['std'][i],
                                            klass['N']) 
        data.append(sample)
        n_samples.append(klass['N'])
    classes = np.repeat(np.arange(len(parameters)), repeats=n_samples)
    data = np.concatenate(data, axis=0)
    return classes, data


def plot_data(parameters, data):
    assert len(parameters) <= 3, 'Cannot plot more than 3 classes'
    i = 0
    colors = ['r', 'g', 'b']
    for n_klass, klass in enumerate(parameters):
        plt.plot(*data[i:i+klass['N']].T, marker='o', color=colors[n_klass], ls='')
        i += klass['N']
    plt.show()


def evaluate():
    parameters = [
        {'mean': [1, 1], 'std': [0.5, 1], 'N': 100},
        {'mean': [1, 3], 'std': [1, 1], 'N': 150},
        {'mean': [3, 2], 'std': [0.5, 0.5], 'N': 200}
        ]
    classes, data = sample_data(parameters)
    plot_data(parameters, data)
    results = abx_numpy.abx(classes, data, lambda x, y: np.linalg.norm(x - y))
    np.save('results.npy', results[2])
    print results[0]


evaluate()
