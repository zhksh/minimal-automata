#!/usr/bin/python3
"""
Entry file for the MinDict Implementation.
"""

from argparse import ArgumentParser
from daciuk import MinDict
from Tarjantable import Tarjantable
from draw import draw_automaton
from ui_strings import MESSAGES


def main():
    """
    Central user interface.
    """

    # Parse arguments
    parser = ArgumentParser(description="Minimaler Lexikonautomat, Basismodul CL WS 20/21")
    parser.add_argument(
        "-wl",
        "--wordlist",
        type=str,
        default="wl.test",
        # default="wordlist.txt",
        help="Path to the sorted wordlist")
    args = parser.parse_args()

    # read wordlist
    words = list()
    try:
        words = open(args.wordlist).read().splitlines()
    except FileNotFoundError:
        print(f"ERROR:\n  '-> File {args.wordlist} not found!")
        return

    # build automaton
    min_dict = MinDict(words)

    # interact with the user
    language = "de"
    while True:
        print(
            MESSAGES[language]["welcome"]
        )
        inputted = input(MESSAGES[language]["input"])
        inputted = 3

        if inputted == "1":
            word = input(MESSAGES[language]["wordinput"])
            if min_dict.is_in_dict(word):
                print(f"\n\033[92m\"{word}\"\033[0m " + MESSAGES[language]["wordInLang"] + "\n")
            else:
                print(f"\n\033[91m\"{word}\"\033[0m " + MESSAGES[language]["wordNotInLang"] + "\n")
            continue

        if inputted == "2":
            figure = draw_automaton(min_dict)
            figure.render('graphviz/aut.gv', view=True)
            print("\n\033[96m" + MESSAGES[language]["saved"] + "\033[0m\n")
            continue

        if inputted == "3":
            tt = Tarjantable(trie=min_dict)

            print("\n\033[96m" + MESSAGES[language]["saved"] + "\033[0m\n")
            continue

        if inputted == "X":
            print(MESSAGES[language]["bye"])
            break
        print("\n\033[91m" + MESSAGES[language]["warning"] + "\033[0m\n")


if __name__ == "__main__":
    main()
