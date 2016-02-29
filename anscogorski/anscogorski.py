#!/usr/bin/env python

"""
Demonstrates differences between the Anscombe and Ostrogorski paradoxes in
voting.
"""

from __future__ import division, print_function
import numpy as np


def party_result(votes):
    """
    Given a (voters x issues) matrix,
    returns True if a majority of the voters approve of the issues.
            Issue 1 Issue 2 Issue 3 sum
    Voter 1 True    True    False   True
    Voter 2 True    False   True    True
    Voter 3 False   False   False   False
                                    return True
    """
    n_voters = votes.shape[0]
    return sum(np.mean(votes, axis=1) > 0.5) > n_voters / 2


def issue_result(votes):
    """
    Given a (voters x issues) matrix,
    returns True if a majority of the issues are approved by voters.

            Issue 1 Issue 2 Issue 3
    Voter 1 True    True    False
    Voter 2 True    False   True
    Voter 3 False   False   False
    sum     True    False   False   return False
    """
    n_issues = votes.shape[1]
    return sum(np.mean(votes, axis=0) > 0.5) > n_issues / 2


def voters_frustration(votes):
    """
    Given a (voters x issues) matrix,
    calculate society's decision on each issue
    and return a (voters x frustated-decisions) matrix in which
      1 indicates the voter is "frustrated" with society's decision and
      0 indicates the voter is satisifed.
    """

    # Society's decision on each issue.
    issue_decision = np.mean(votes, axis=0) > 0.5

    # On which issues do the voters differ from society's decision?
    return votes ^ issue_decision


def societal_frustration(votes):
    """
    Given a (voters x issues) matrix,
    calculate which issues "frustrate" the voter (their minority preferences)
    and return a Boolean vector indicating which voters are frustrated
    with most decisions made by society.
    """

    # On how many issues do the voters differ from society's choice?
    num_frustrations = np.sum(voters_frustration(votes), axis=1)

    # Is each voter frustrated on more than half the issues?
    n_issues = votes.shape[1]
    return num_frustrations > n_issues / 2


def anscombe(votes):
    """ Returns True if votes (voters x issues) has the Anscombe paradox. """

    # Are the majority of voters frustrated on the majority of issues?
    n_voters = votes.shape[0]
    return sum(societal_frustration(votes)) > n_voters / 2


def ostrogorski(votes):
    """
    Returns True if votes (voters x issues) has the Ostrogorski paradox.
    """

    return issue_result(votes) != party_result(votes)


def ostrogorski_strict(votes):
    """
    Returns True if votes (voters x issues) has the strict version of the
    Ostrogorski paradox, which means the majority party is in the minority
    on all issues.
    """

    winning_party = party_result(votes)

    return all((np.mean(votes, axis=0) > 0.5) != winning_party)


def describe(votes):
    """
    Prints description of (voters x issues) matrix.
    """

    print()
    print("Votes:")
    print(votes)

    n_votes_cast = votes.shape[0] * votes.shape[1]
    n_votes_1 = votes.sum()
    print("All preferences:     {:.1%}".format(n_votes_1 / n_votes_cast))

    print('Issue decision:      %s' % issue_result(votes))
    print('Party decision:      %s' % party_result(votes))

    print("Ostrogorski paradox: %s" % ostrogorski(votes))
    print("O-Strict paradox:    %s" % ostrogorski_strict(votes))

    print("Voters' frustration:")
    print(voters_frustration(votes))

    print('Societal frustration %s' % societal_frustration(votes))

    print('Anscombe paradox:    %s' % anscombe(votes))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--voters', metavar='N', type=int, default=5,
                        help="number of voters")
    parser.add_argument('--issues', metavar='N', type=int, default=3,
                        help="number of issues")
    args = parser.parse_args()

    # Iterate through a variety of voter x issue preference combos.
    from itertools import product, combinations_with_replacement

    # All possible preferences for a voter.
    preference_lists = list(product([0, 1], repeat=args.issues))

    # Voters with various combinations of preferences.
    for votes in combinations_with_replacement(preference_lists, args.voters):
        describe(np.array(votes))


if __name__ == '__main__':
    main()
