#!/usr/bin/python3
"""
Entry file for the MinDict Implementation.
"""

from argparse import ArgumentParser
from daciuk import MinDict
from draw import draw_automaton
from ui_strings import MESSAGES

def save(object, filename):
    import pickle
    with open(filename, 'wb') as file:
        pickle.dump(object, file, pickle.HIGHEST_PROTOCOL)

def load(object, filename):
    import pickle
    with open(filename, 'rb') as file:
        object = pickle.load(file)
        return object

def file_exists(filename) -> bool:
    import os.path
    return os.path.isfile(filename)


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

    filename = "automaton.pkl"
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
        print(MESSAGES[language]["welcome"])
        print("{}{}".format("\t", MESSAGES[language]["options"]["check_word"]))
        print("{}{}".format("\t", MESSAGES[language]["options"]["draw_automaton"]))
        print("{}{}".format("\t", MESSAGES[language]["options"]["save"]))
        if file_exists(filename):
            print("{}{}".format("\t", MESSAGES[language]["options"]["load"]))


        choice = input(MESSAGES[language]["input"])
        # inputted = "3"

        if choice == "1":
            word = input(MESSAGES[language]["wordinput"])
            if min_dict.is_in_tarjan_table(word):
                print(f"\n\033[92m\"{word}\"\033[0m " + MESSAGES[language]["wordInLang"] + "\n")
            else:
                print(f"\n\033[91m\"{word}\"\033[0m " + MESSAGES[language]["wordNotInLang"] + "\n")
            continue

        if choice == "2":
            figure = draw_automaton(min_dict)
            figure.render('graphviz/aut.gv', view=True)
            print("\n\033[96m" + MESSAGES[language]["saved"] + "\033[0m\n")
            continue

        if choice == "3":
            save(min_dict, filename)
            print("\n\033[96m" + MESSAGES[language]["automaton_saved"] + "\033[0m\n")
            continue

        if choice == "4":
            min_dict = load(min_dict, filename)
            print("\n\033[96m" + MESSAGES[language]["automaton_loaded"] + "\033[0m\n")
            continue

        if choice == "X":
            print(MESSAGES[language]["bye"])
            break

        print("\n\033[91m" + MESSAGES[language]["warning"] + "\033[0m\n")


if __name__ == "__main__":
    main()

