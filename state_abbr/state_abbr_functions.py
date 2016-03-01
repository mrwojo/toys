#!/usr/bin/env python

"""
A variety of techniques for abbreviating US state names.

TODO: Refactor to make it clearer that the abbreviation functions are more
like abbreviation *models* in that their output depends on the whole set of
input names and proposed output abbreviations.
"""

from __future__ import print_function
import string
from itertools import izip_longest
from state_abbr import state2abbr
from collections import Counter


def second_letters(text):
    """
    Given a single word: returns the letters after the first letter.
    Given 2 or more words: returns the letters starting from the second word,
    then it wraps around to the first word.

    This is used for abbreviation patterns like "AS" for "American Samoa".
    The "S" is the first letter of the second word.

    >>> second_letters("American Samoa")
    'Samoamerican'
    """
    space = text.find(" ")

    if space == -1:
        return text[1:]
    else:
        return text[space+1:] + text[1:space]


def words_letters(text):
    """
    Traverse words then letters order. Returns a generator.

    >>> ''.join(words_letters("Aa B Ccc"))
    'ABCacc'
    """
    # This goes in words then letters order.
    words = text.split()

    for group in izip_longest(*words):
        for c in group:
            if c is not None:
                yield c


def abbr_usps(names):
    """
    Abbreviates the state names the official way. This is not a general
    abbreviator: it works only for state names.

    >>> list(abbr_usps(["Pennsylvania"]))
    ['PA']

    >>> list(abbr_usps(["Foo"]))
    Traceback (most recent call last):
        ...
    KeyError: 'Foo'
    """
    for name in names:
        yield state2abbr[name]


def abbr_trivial(names):
    """
    Abbreviation is simply the first 2 letters of the name.

    >>> list(abbr_trivial(["Pennsylvania"]))
    ['PE']
    """
    for name in map(string.upper, names):
        yield name[:2]


def abbr_no_dupes(names):
    """
    Abbreviation is the first letter plus any letter from the name that makes
    this abbreviation unique with respect to already-abbreviated items.

    Alabama gets "AL" (the first 2 letters).
    Alaska gets "AA" because the 2nd letter, L, is already taken.

    >>> list(abbr_no_dupes(["Abc", "Acd", "Ace"]))
    ['AB', 'AC', 'AE']

    A failure:

    >>> list(abbr_no_dupes(["Abc", "Abd", "Adb"]))
    ['AB', 'AD', 'AB']

    "Abc" squanders the "AB" abbreviation.
    """
    abbrs = set()

    for name in map(string.upper, names):
        for c in second_letters(name):
            abbr = name[0] + c

            # Stop on the first unseen abbreviation.
            if abbr not in abbrs:
                break

        yield abbr
        abbrs.add(abbr)


def abbr_first_in_order(names):
    """
    The second letter of this abbreviation comes from the first
    character that would put this abbreviation in order relative to
    the previous abbreviation.

    >>> list(abbr_first_in_order(['Abc', 'Abd']))
    ['AB', 'AD']

    This approach fails for the existing list of names:
        Alabama -> AL
        Alaska -> AS
            "S" is the first character in the name that succeeds the
            "L" from the previous abbreviation.
        American Samoa -> ??
            "MERICAN SAMOA" contains no letters that come after "S".

    >>> list(abbr_first_in_order(['Zz', 'Zza']))
    ['ZZ', 'ZA']
    """
    prev_abbr = ""
    for name in map(string.upper, names):
        # Abbr is the first letter plus the next character that would
        # produce an abbreviation that follows the prev_abbr.
        for c in second_letters(name):
            abbr = name[0] + c

            if abbr > prev_abbr:
                break

        yield abbr
        prev_abbr = abbr


def abbr_least(names):
    """
    Abbreviation is the first letter plus the next non-repeat letter that is
    closest in ordering to the previous abbreviation.

    >>> list(abbr_least(["Abc", "Azc"]))
    ['AB', 'AC']

    TODO: This can fail in some cases that I haven't yet localized.
    """

    prev_abbr = "AA"
    for name in map(string.upper, names):
        min_abbr = None

        for c in second_letters(name):
            abbr = name[0] + c

            if abbr > prev_abbr \
                    and (min_abbr is None or abbr < min_abbr) \
                    and abbr[0] != abbr[1]:
                min_abbr = abbr

        yield min_abbr
        prev_abbr = min_abbr


def abbr_most_unusual(names):
    """
    Abbreviation is the first letter plus the next non-repeat letter that is
    most unusual among names.

    >>> list(abbr_most_unusual(["Abd", "Acd", "Ade"]))
    ['AB', 'AC', 'AE']

    "E" is more unusual than "D", which appears in every name.

    TODO: Use letter_freq for "unusual among English letters"
    """

    name_letter_freq = Counter()

    for name in map(string.upper, names):
        name_letter_freq.update(name)

    for name in map(string.upper, names):
        min_abbr = (float('inf'), None)

        for c in second_letters(name):
            abbr = name[0] + c
            score = name_letter_freq[c]

            if score < min_abbr[0] and abbr[0] != abbr[1]:
                min_abbr = (score, abbr)

        yield min_abbr[1]


def abbr_unique_pairs(names):
    """
    Abbreviation starts with the first letter and the second letter is the
    least common letter among names starting with the first letter.

    Whereas abbr_most_unusual is based on overall letter frequencies, this is
    based on frequencies only among names starting with the same letter.

    abbr_unique_pairs uses "QD" because "D" is not common in names starting
    with "Q".

    >>> list(abbr_unique_pairs(["Abd", "Acd", "Qvd", "Qvz"]))
    ['AB', 'AC', 'QD', 'QZ']

    abbr_most_unusual uses "QV" because "D" is more frequent in all names (3)
    than "V" (2).

    >>> list(abbr_most_unusual(["Abd", "Acd", "Qvd", "Qvz"]))
    ['AB', 'AC', 'QV', 'QZ']
    """

    abbr2names = {}
    name2abbrs = {}

    for name in names:
        upper_name = name.upper()
        a = upper_name[0]

        for b in upper_name[1:]:
            if b in string.letters and a != b:
                abbr2names.setdefault(a + b, set()).add(name)
                name2abbrs.setdefault(name, set()).add(a + b)

    for name in names:
        abbrs = name2abbrs[name]
        count_abbrs = []

        for abbr in abbrs:
            count_abbrs.append((len(abbr2names[abbr]), abbr))

        count_abbrs.sort()

        # print("%25s  %s" % (name, " ".join(str(c)+a for c,a in count_abbrs)))
        # print("%25s  %s" % (name, " ".join(a for c,a in count_abbrs if c == 1)))

        yield count_abbrs[0][1]


def is_ordered(seq):
    """ Returns True if the sequence is in order. """
    return tuple(seq) == tuple(sorted(seq))


def is_monotonic(*seqs):
    """
    Given a bunch of sorted tuples (x0, y0), (x1, y1), ...,
    this returns True if the alpha-ordering of x0, x1, ...
    is equal to the alpha-ordering of y0, y1, ...
    """

    for a in zip(*seqs):
        if not is_ordered(a):
            return False
    return True


def has_duplicates(seq):
    """ Returns True if the sequence contains duplicate items. """
    return len(seq) != len(set(seq))


def main():
    abbr_functions = [
        abbr_usps,
        abbr_trivial,
        abbr_first_in_order,
        abbr_no_dupes,
        abbr_least,
        abbr_most_unusual,
        abbr_unique_pairs,
    ]

    names = sorted(state2abbr.keys())

    all_abbrs = {'': names}

    for abbr_function in abbr_functions:
        function_name = abbr_function.__name__[len('abbr_'):]

        all_abbrs[function_name] = list(abbr_function(names))

    from tabulate import tabulate
    print(tabulate(all_abbrs, headers='keys'))

    # TODO: output evaluations of these abbreviations
    #  - successful abbreviation of all names? (there's at least 1 "None")
    #  - monotonic alpha-order?
    #  - unique abbreviations of all names?


if __name__ == '__main__':
    main()
