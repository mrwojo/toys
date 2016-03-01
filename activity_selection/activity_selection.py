#!/usr/bin/env python

"""
Illustrates greedy activity selection.
"""

from __future__ import print_function
from collections import namedtuple
from random import randint


Activity = namedtuple('Activity', 'start finish')


def argsort(lst):
    """
    Like NumPy's argsort: returns the indices that would sort the input list.
    """
    return [v[0] for v in sorted(enumerate(lst), key=lambda v: v[1])]


def select_activities_greedy(activities):
    """
    Given a list of activities, possibly with conflicting start/end times,
    return a list of indices of selected activities.

    According to the activity selection problem, the length of the output list
    should be maximized.
    """

    # List of indices corresponding to activities sorted by their finish time.
    sorted_activities = argsort(v.finish for v in activities)

    # Initialize selected activity list with the activity that'll end soonest.
    selected = [sorted_activities[0]]
    curr_time = activities[selected[0]].finish

    # Select non-conflicting activities.
    for i in sorted_activities[1:]:
        if activities[i].start >= curr_time:
            selected.append(i)
            curr_time = activities[i].finish

    return selected


def random_activity():
    """ Returns an activity with random start and end time. """
    start = randint(0, 4)
    duration = randint(1, 4)
    return Activity(start, start + duration)


def random_activities(n):
    """ Returns n activities with random start and end times. """
    return [random_activity() for _ in xrange(n)]


def main():
    from pprint import pprint

    activities = random_activities(10)
    pprint(activities)

    selected = select_activities_greedy(activities)
    pprint(selected)

    pprint([activities[i] for i in selected])


if __name__ == '__main__':
    main()
