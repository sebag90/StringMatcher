import re
import unittest

import src.naive_matcher as nv
import src.ahoc_automaton as ac

"""
This file contains the tests for this projects
Where possible, golden standards are given by the re
module from python
"""


class Test(unittest.TestCase):

    strings = [
        "this is only the beginning of the testing",

        ("The PRADA Christmas Race is a one day knock out series, "
            "based on the seeding from the PRADA ACWS Auckland, NZ and "
            "the last chance for teams to take on the Defender before the "
            "36th America’s Cup Presented by PRADA."),

        ("A sailing HYDROFOIL, hydrofoil sailboat, or hyDRosail is a "
            "sailboat with wing-like foils mounted under the hull"),

        "bottle BOTTLE bottle BOTTLE bottle BOTTLE"
    ]

    patterns = [
        "th",
        "PRADA",
        "hydro",
        "bottle"
    ]

    case_insensitive = [
        True,
        False,
        True,
        False
    ]

    def test_single_pattern(self):
        # for each string the algorithms should match one single pattern
        gold = []
        ac_matches = []
        naive_matches = []

        for string, pattern, case in zip(self.__class__.strings,
                                         self.__class__.patterns,
                                         self.__class__.case_insensitive):

            if case:
                pattern = pattern.lower()

            # create objects
            naive_matcher = nv.NaiveStringMatcher([pattern])
            ac_matcher = ac.State.create_automaton([pattern])

            # match string
            naive_matcher.find_match(string, case)
            ac_matcher.find_match(string, case)

            # append results
            ac_matches.append(ac_matcher.results[pattern])
            naive_matches.append(naive_matcher.results[pattern])

            # calculate gold
            if case:
                string = string.lower()

            a = re.finditer(pattern, string)
            gold.append([i.start() for i in a])

        self.assertListEqual(gold, ac_matches)
        self.assertListEqual(gold, naive_matches)

    def test_multiple_pattern(self):
        # for each string the algorith should match all patterns

        gold = []
        ac_matches = []
        naive_matches = []

        for string, _, case in zip(self.__class__.strings,
                                   self.__class__.patterns,
                                   self.__class__.case_insensitive):

            if case:
                patterns = [i.lower() for i in self.__class__.patterns]

            # create objects
            naive_matcher = nv.NaiveStringMatcher(patterns)
            ac_matcher = ac.State.create_automaton(patterns)

            # match string
            naive_matcher.find_match(string, case)
            ac_matcher.find_match(string, case)

            # calculate gold
            gold_results = {}

            if case:
                string = string.lower()

            for pattern in patterns:
                a = re.finditer(pattern, string)
                result = ([i.start() for i in a])
                if result:
                    gold_results[pattern] = result

            gold.append(gold_results)
            ac_matches.append(ac_matcher.results)
            naive_matches.append(naive_matcher.results)

        self.assertListEqual(gold, naive_matches)
        self.assertListEqual(gold, ac_matches)

    def test_multiple_counting(self):
        # for each string the algorith should match all patterns

        gold = []
        ac_matches = []
        naive_matches = []

        for string, pattern, case in zip(self.__class__.strings,
                                         self.__class__.patterns,
                                         self.__class__.case_insensitive):

            if case:
                patterns = [i.lower() for i in self.__class__.patterns]

            # create objects
            naive_matcher = nv.NaiveStringMatcher(patterns)
            ac_matcher = ac.State.create_automaton(patterns)

            # match string
            naive_matcher.find_match(string, case)
            ac_matcher.find_match(string, case)

            # calculate gold
            gold_results = {}

            if case:
                string = string.lower()

            for pattern in patterns:
                a = re.findall(pattern, string)
                result = len(a)

                # my algorithms only save patterns if
                # they actually are in the text
                if result:
                    gold_results[pattern] = result

            gold.append(gold_results)
            ac_matches.append(ac_matcher.counts)
            naive_matches.append(naive_matcher.counts)

        self.assertListEqual(gold, naive_matches)
        self.assertListEqual(gold, ac_matches)

    def test_single_counting(self):
        # for each string the algorithms should match one single pattern

        gold = []
        ac_matches = []
        naive_matches = []

        for string, pattern, case in zip(self.__class__.strings,
                                         self.__class__.patterns,
                                         self.__class__.case_insensitive):

            if case:
                pattern = pattern.lower()

            # create objects
            naive_matcher = nv.NaiveStringMatcher([pattern])
            ac_matcher = ac.State.create_automaton([pattern])

            # match string
            naive_matcher.find_match(string, case)
            ac_matcher.find_match(string, case)

            # append results
            ac_matches.append(ac_matcher.counts[pattern])
            naive_matches.append(naive_matcher.counts[pattern])

            # calculate gold
            if case:
                string = string.lower()

            a = re.findall(pattern, string)
            gold.append(len(a))

        self.assertListEqual(gold, ac_matches)
        self.assertListEqual(gold, naive_matches)


if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)
