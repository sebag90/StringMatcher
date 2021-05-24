"""
StringMatcher is the main class of my programme.
Based on the type of input from the user (pattern, text,
naive, case sensitive, json or counter) the class instanciate
the correct matching algorithm and formats the output in
a readable way
"""

import json
from pathlib import Path
import sys
import os

from src.naive_matcher import NaiveStringMatcher
from src.ahoc_automaton import State


class StringMatcher():

    def __init__(self, pattern, text, naive, case, recursive, json, counter):
        self.patterns = self.extract_pattern(pattern)
        self.text = text
        self.naive = naive
        self.case_insensitive = case
        self.__results = {}
        self.recursive = recursive
        self.json = json
        self.input = []
        self.counter = counter
        self.errors = []
        self.first_print = True
        self.text_type = self.define_text_type()
        self.json_results = {}
        self.validate_data()

    def extract_pattern(self, patterns):
        """
        given the argument PATTERN from the argument parser,
        this function decides if it's a single pattern or a
        file. If it's a file, each line is a search pattern.

        Parameters:
            - argument (string): user input for PATTERN

        Returns:
            - patterns (list): a list of patterns to initialize
                the matching algorithm
        """

        # if we have more patterns or
        # a single one which is not a file:
        if len(patterns) > 1 or (
           len(patterns) == 1 and not os.path.isfile(patterns[0])):
            return patterns

        else:
            pattern = patterns[0]
            pat_list = []
            # if PATTERN is a file, extract all patterns
            if os.path.isfile(pattern):
                try:
                    with open(pattern, "r", encoding="utf-8") as p_file:
                        for line in p_file:
                            pat_list.append(line.strip())
                except Exception:
                    print("The selected PATH-file cannot be opened! "
                          "Please choose another one.")
                    sys.exit()

            return pat_list

    def define_text_type(self):
        """
        this function unifies the input format for the TEXT parameter
        and divides it in 2 options:
        - file:
            the input needs to be opened
            works for single file and directory, it saves in self.input
            a list of paths in format (path, filename)

        - string:
            the input is already in string file
            it saves it in a list of strings

        it returns a string (file or string) for better
        readability (instead of checking during unpacking if data type
        is a tuple or a string)
        """
        # only one text
        if len(self.text) == 1:
            text = self.text[0]

            # DIRECTORY
            if os.path.isdir(text):
                # retrieve files
                file_list = []

                # only fetch files in this folder
                for path, _, files in os.walk(text):
                    if self.recursive is False:
                        if path == text:
                            for filename in files:
                                filepath = Path(f"{path}/{filename}")
                                file_list.append((filepath, filename))

                    # recursively fetch all files
                    else:
                        for filename in files:
                            filepath = Path(f"{path}/{filename}")
                            file_list.append((filepath, filename))

                file_list.sort()
                self.input = file_list
                return "file"

            # SINGLE FILE
            elif os.path.isfile(text):
                filepath = Path(text)
                self.input.append((filepath, None))
                return "file"

            # STRING
            else:
                self.input.append(text)
                return "string"

        else:
            # MORE STRINGS
            self.input = self.text
            return "string"

    def validate_data(self):
        """
        remove the empty string from the patterns
        if no patterns are left, stops the programme and
        warns the user. No need to validate the TEXT
        parameter as an empty string cannot contain
        any other pattern
        """
        for pattern in self.patterns:
            if pattern == "":
                self.patterns.remove("")

        if not self.patterns:
            print("WARNING! Missing pattern or empty string!")
            sys.exit()

    def choose_algorithm(self):
        """
        a wrapper function to initialize either one of the string macher
        classes to eliminate differences in initialization.
        case sensitive is needed for automaton.

        Returns:
            - the matcher (object)
        """

        # if case insensitive lowercase patterns
        for i in range(len(self.patterns)):
            if self.case_insensitive:
                self.patterns[i] = self.patterns[i].lower()

        # naive matcher option
        if self.naive:
            matcher = NaiveStringMatcher(self.patterns)
            return matcher

        # AHC matcher by default
        matcher = State.create_automaton(self.patterns)
        return matcher

    @staticmethod
    def progress_bar(iteration, total, prefix='', suffix='', decimals=1,
                     length=40, fill='#', miss=".", end="\r", stay=True,
                     fixed_len=False):
        """
        Call in a loop to create terminal progress bar
        Parameters:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            miss        - Optional  : bar missing charachter (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
            stay        - Optional  : progress bar stays on terminal
            fiexed_len  - Optional  : length includes pre- and suffix
        """
        if fixed_len:
            bar_len = length - len(prefix) - len(suffix)
        else:
            bar_len = length

        percent = f"{100*(iteration/float(total)):.{decimals}f}"
        filled_length = int(bar_len * iteration // total)
        bar = f"{fill * filled_length}{miss * (bar_len - filled_length)}"
        to_print = f"\r{prefix} [{bar}] {percent}% {suffix}"
        print(to_print, end=end)

        # Print New Line on Complete
        if iteration >= total:
            if stay:
                print()
            else:
                # clean line given lenght of lase print
                print(" "*len(to_print), end=end)

    @property
    def results(self):
        """
        this functions prepares the output of the programme for a
        single run (either a string or one file)
        based on various parameters (number of patterns, counter,
        number of TEXT parameters) the results will look slightly
        different

        Parameters:
            - results from matcher (saved in self.results)

        Returns:
            - to_print (string):
        """
        to_print = ""

        # determine longest key for pretty print
        limit = 0
        for key in self.__results:
            if len(key) > limit:
                limit = len(key)

        # decide spacing  and ending between results based on type of input
        spacing = ""
        if len(self.input) > 1:
            spacing = "\t"

        for key in self.__results:
            key_name = key
            if len(self.patterns) < 2:
                key_name = ""

            if self.counter:
                matches = self.__results[key]
            else:
                matches = ", ".join([str(i) for i in self.__results[key]])

            if len(self.patterns) > 1:
                to_print += (f'{spacing}{key_name:<{limit+2}}{matches}\n')
            else:
                to_print += (f'{spacing}{matches}\n')

        # remove last newline
        to_print = to_print[:-1]

        return to_print

    def save_json(self):
        with open("results.json", "w", encoding="utf-8") as json_f:
            json.dump(self.json_results, json_f, ensure_ascii=False, indent=4)

    def output(self, argument):
        """
        This functions prints (or saves in JSON) the output from the matcher
        based on some parameters (es. self.recursive, type of input).
        It prints additional informations such as the TEXT string or the name
        of the file and the calls the function self.results to format the rest
        of the output.

        Parameters:
            argument: this is either a tuple (in case of files) or a string

        Returns:
            None, prints the results to the console or saves them json_results
        """
        if not self.json:
            if not self.first_print:
                print()

        self.first_print = False

        if isinstance(argument, tuple):
            filepath, filename = argument

            if not self.json:
                # if -r, print the path AND the name of the file
                # if not only filename, path is given by user
                if filename:
                    to_print = filename
                    if self.recursive:
                        to_print = filepath
                    print(f"- {to_print}")

                print(self.results)

            else:
                # always use complete path as key, otherwise path lost
                # once the file is saved
                self.json_results[str(filepath)] = self.__results

        # string
        else:
            if not self.json:
                # if multiple TEXTS, print TEXT
                if len(self.input) > 1:
                    print(f"- {argument}")
                print(self.results)

            else:
                self.json_results[argument] = self.__results

    def process_files(self):
        """
        This function processes the input which comes in form of a file.

        Parameters:
            self.input (list of tuples (path, filename))

        Returns:
            saves the results from the matcher in self.__results
        """
        matcher = self.choose_algorithm()
        # process one file at the time for better memory management
        for i, element in enumerate(self.input):
            filepath, _ = element

            try:
                with open(filepath, "r", encoding="utf-8") as readfile:
                    for line in readfile:
                        matcher.find_match(line, self.case_insensitive)

            # collect unreadeable files for error log
            except Exception:
                self.errors.append(str(filepath))

            # copy results and reset matcher for next file
            self.__results = matcher.results

            if self.counter:
                self.__results = matcher.counts

            matcher.reset()

            # output - print or json
            if self.results:
                self.output(element)

            # if json print progress bar
            if self.json:
                self.progress_bar(i+1, len(self.input), prefix="Matching:",
                                  fixed_len=True, length=40)

    def process_strings(self):
        """
        This function processes the input which comes in form of a string.

        Parameters:
            self.input (list strings)

        Returns:
            saves the results from the matcher in self.__results
        """
        for string in self.input:
            matcher = self.choose_algorithm()
            matcher.find_match(string, self.case_insensitive)
            self.__results = matcher.results

            if self.counter:
                self.__results = matcher.counts

            if self.__results:
                self.output(string)

    def run(self):
        """
        the 'main' function of the class, given the type of input
        it calls the appropriate function to process it
        """
        # FILE INPUT
        if self.text_type == "file":
            self.process_files()

        # STRING INPUT
        else:
            self.process_strings()

        if self.json:
            self.save_json()

        if self.errors:
            print("\nThe following file(s) could not be opened:")
            for error in self.errors:
                print(f"\t{error}")
