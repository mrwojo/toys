#!/usr/bin/env python

"""
Visualize centroids for a given set of 2D points and a variety of weights.

The centroid of points is their arithmetic mean. Just as the mean can be
extended to a weighted mean, you can also have weighted centroids, where each
point is assigned a different weight in the average.

This script illustrates that a straightforward sequence of weights (such as
[1, 2, 3, ...]) produces centroids that fall into some interesting patterns.

The symmetry is related to using the same set of weights for each point.
Lines and arcs may be related to the small set of weights that produce the many
combinations of weights (similar to effects of a posterized image).

Implementation note: sklearn.utils.extmath.cartesian() is faster than product()
but it's not significant enough to drag in sklearn.

Run:
    ./weightedcentroids.py
    Matplotlib scatterplot should appear.

    ./weightedcentroids.py images
    Writes scatterplots to *.png files in curr directory.

Mark Wojtowicz
License: CC0

TODO: Random weights; refactor (argparse, weighted centroid function)
"""

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import sys


def main():
    # Triangle point pattern
    points_x = np.array([0, 0.5, 1])
    points_y = np.array([0, 1.0, 0])

    # Create some sequences that'll form the weights.
    # Small (<50) for performance: num. centroids grows as steps**len(points).
    steps = 35

    lin_s = np.linspace(1. / steps, 1.0, steps)
    log_s = np.logspace(1. / steps, 1.0, steps)

    # weight sequences
    sequences = [
        ('linear', lin_s),
        ('linear-squared', lin_s**2),
        ('linear-inverse', lin_s**-1),
        ('logarithmic', log_s),
    ]

    num_weights = steps ** len(points_x)

    print('# weights {:,d}  (= {:,d}**{:,d} = steps**len(points))'.format(
        num_weights, steps, len(points_x)))

    # NumPythonic: Repeat the points weights times for np.average
    multipoints_x = np.repeat([points_x], num_weights, axis=0)
    multipoints_y = np.repeat([points_y], num_weights, axis=0)

    for i, (sequence_name, sequence) in enumerate(sequences):
        print(sequence_name)

        # Weights are the Cartesian product of sequence x sequence x ... x
        # sequence, for as many sequences as there are points.
        weights = np.array(list(product(sequence, repeat=len(points_x))))

        centroids_x = np.average(multipoints_x, weights=weights, axis=1)
        centroids_y = np.average(multipoints_y, weights=weights, axis=1)

        # Visualize
        plt.title(sequence_name + " weights")
        plt.scatter(centroids_x, centroids_y,
                    s=2, marker='.', lw=0, label='Centroids')
        plt.scatter(points_x, points_y, c='r', marker='+')
        plt.legend()

        if sys.argv[-1] == 'images':
            out_name = 'weightedcentroids-%s.png' % sequence_name
            print('writing', repr(out_name))
            plt.savefig(out_name)
        else:
            plt.show()

        plt.close()


if __name__ == '__main__':
    main()
