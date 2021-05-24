import time


class NaiveStringMatcher:

    def __init__(self, patterns):
        self.patterns = patterns
        self.results = {}
        self.__counter = 0
        self.counts = {}

    def reset(self):
        """
        This function delets results, counts and the counter.
        Only the patterns are kept - used to search the same
        patterns in another text
        """
        self.results = {}
        self.__counter = 0
        self.counts = {}

    def find_match(self, line, case_insensitive=False):
        """
        slide a window of length of the pattern over the string,
        if the windows is equal to the word then saves the index

        -----
        Parameters:
            - line: string, the line to be searched

        Returns:
            -void (saves the index where the matches begins in
                   self__results, index is of type integer)
        """

        if case_insensitive:
            line = line.lower()

        for pattern in self.patterns:
            for i in range(len(line) - len(pattern) + 1):
                window = line[i:i + len(pattern)]
                if pattern == window:
                    if pattern not in self.results:
                        self.results[pattern] = []

                    if pattern not in self.counts:
                        self.counts[pattern] = 0

                    self.results[pattern].append(i + self.__counter)
                    self.counts[pattern] += 1
        self.__counter += len(line)

    def demo(self, line):
        for pattern in self.patterns:
            for i in range(len(line) - len(pattern) + 1):

                e = "\r"
                if i == len(line) - len(pattern):
                    e = "\n"

                window = line[i:i + len(pattern)]
                match_found = " --> MATCH"

                if window != pattern:
                    afterline = " " * len(match_found)
                else:
                    afterline = match_found

                print(f"{line[0:i]}[{window}]"
                      f"{line[i+len(pattern):]}{afterline}", end=e)

                time.sleep(0.3)


if __name__ == "__main__":
    text = "I am Curiouser and Curiouser!"
    pattern = "Curious"
    print(f"Text: {text}")
    print(f"We want to find the indeces of this pattern: {pattern}")
    print("by sliding a window over the text and to see if we can find it:\n")
    s = NaiveStringMatcher([pattern])
    s.find_match(text)
    s.demo(text)
    print("\nand this is the result:")
    for key in s.results:
        print(f"{key:<10}{s.results[key]}")

    print("\nthe matcher also counts the absolute frequency:")
    for key in s.results:
        print(f"{key:<10}{s.counts[key]}")
