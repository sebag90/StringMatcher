import time
from pathlib import Path

from src.ahoc_automaton import State
from src.naive_matcher import NaiveStringMatcher


def speed(patterns, filename):
    """
    given a list of patterns and a file this function calculates the time
    needed for each algorithm to find all the patterns in the text.
    Results are then compared and if both pattern matcher yield the same
    result, the function prints out the time it took for each algorithm
    to find all results and the time increase in percentage from the
    fastest to the slowest algorithm
    """

    # Aho-Corasick
    start_aho = time.time()
    a = State.create_automaton(patterns)
    with open(filename, "r") as f:
        for line in f:
            a.find_match(line)
    t_aho = time.time() - start_aho

    # naive
    start_naive = time.time()
    n = NaiveStringMatcher(patterns)
    with open(filename, "r") as f:
        for line in f:
            n.find_match(line)
    t_naive = time.time() - start_naive

    assert n.results == a.results

    min_n = min(t_aho, t_naive)
    max_n = max(t_aho, t_naive)
    inc = ((max_n - min_n)/min_n)*100

    print(f"PATTERNS: {len(patterns):<3}- TIME(s): AHC: {t_aho:<8.3f}"
          f"NAIVE: {t_naive:<8.3f}DIFF: {inc:.2f}%")


def main():
    patterns = [
        "pavlograd",
        "ulceration",
        "exostoses",
        "zygomatic",
        "Kutuzov",
        "Braunau",
        "Pierre",
        "boom",
        "cottage",
        "Schoss",
        "Natasha",
        "countermovement",
        "commonwealth",
        "limbs",
        "charmingly"
        "Mamma",
        "Doctrines",
        "Parliament",
        "Dissenters",
        "Pennsylvania",
        "women",
        "Copyright",
        "eBooks",
        "Bohemia",
        "Beeches",
        "Peculiar",
        "certificates",
        "Serpentine",
        "PROGRESSIVE",
        "primaries",
        "University"
    ]

    """ Download: http://norvig.com/big.txt"""
    filename = Path("data/big.txt")

    n = (1, 3, 5, 7, 12, 18, 24, 30)

    for limit in n:
        speed(patterns[:limit], filename)


if __name__ == "__main__":
    main()
