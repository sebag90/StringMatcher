import argparse
from src.string_matcher import StringMatcher


def main():
    # argument parser
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    # required arguments
    required = parser.add_argument_group("required arguments")

    help_pattern = "the pattern to match, can be multiple strings or a file"
    required.add_argument("-p", "--pattern", help=help_pattern, nargs="+",
                          metavar="PATTERN", action="store", required=True)

    help_text = ("text to be searched, can be multiple strings, "
                 "a single file or a directory")
    required.add_argument("-t", "--text", help=help_text, metavar="TEXT",
                          nargs="+", action="store", required=True)

    # optional arguments
    optional = parser.add_argument_group('optional arguments')

    help_insensitive = "case insensitive search"
    optional.add_argument("-i", "--insensitive", help=help_insensitive,
                          action="store_true")

    help_naive = "naive algorithm"
    optional.add_argument("-n", "--naive", help=help_naive,
                          action="store_true")

    help_recursive = "recursively look for all files in TEXT folder"
    optional.add_argument("-r", "--recursive", help=help_recursive,
                          action="store_true")

    help_json = "save results in a json file"
    optional.add_argument("-j", "--json", help=help_json, action="store_true")

    help_counter = "print counts of matches instead of indeces"
    optional.add_argument("-c", "--counter", help=help_counter,
                          action="store_true")

    args = parser.parse_args()

    # collect arguments
    text = args.text
    pattern = args.pattern
    naive = args.naive
    case = args.insensitive
    recursive = args.recursive
    json = args.json
    counter = args.counter

    # instanciate the matcher and run it
    sucher = StringMatcher(pattern, text, naive, case, recursive, json, counter)
    sucher.run()


if __name__ == "__main__":
    main()
