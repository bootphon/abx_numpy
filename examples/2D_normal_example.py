"""
This example apply the abx evaluation on 2D data sampled from gaussian distributions (diagonal covariance)
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
        plt.plot(*data[i:i+klass['N']].T, marker='o', color=colors[n_klass], ls='', label='class {}'.format(n_klass))
        i += klass['N']
    plt.legend(numpoints=1)
    plt.title('Normally distributed data points (diagonal covariance)')
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
    print results


if __name__ == '__main__':
    evaluate()    
