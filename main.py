#!/usr/bin/python3 -u
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


def read_file_generator(fh, blocksize):
    lines = []
    for line in fh:
        lines.append(line)
        if len(lines) == blocksize:
            yield lines
            lines = []
    yield lines

# def find_in_file(fh, string):
#     lines = fh.read().splitlines()
#     for l in lines:
#         if string == l: return True
#     return False


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
        # default="wl.test",
        default="wordlist.txt",
        help="Path to the sorted wordlist")
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        default="automaton.pkl",
        help="Filename for saved automaton")
    parser.add_argument(
        "-bs",
        "--blocksize",
        type=int,
        default=100,
        help="Blocksize for data generator")
    args = parser.parse_args()

    # build automaton
    min_dict = None
    tarjan = None

    # interact with the user
    language = "de"
    allowed_options = set("X")
    while True:
        print(MESSAGES[language]["welcome"])
        if min_dict is None:
            print("{}{}".format("\t", MESSAGES[language]["options"]["compute"]))
            allowed_options.add("0")
        if tarjan is not None:
            print("{}{}".format("\t", MESSAGES[language]["options"]["check_word"]))
            allowed_options.add("1")
            print("{}{}".format("\t", MESSAGES[language]["options"]["save"]))
            allowed_options.add("3")
        if min_dict is not None:
            print("{}{}".format("\t", MESSAGES[language]["options"]["draw_automaton"]))
            allowed_options.add("2")

        if file_exists(args.filename):
            print("{}{}".format("\t", MESSAGES[language]["options"]["load"]))
            allowed_options.add("4")
        print("{}{}".format("\t", MESSAGES[language]["options"]["exit"]))


        choice = input(MESSAGES[language]["input"])

        if choice in allowed_options:
            if choice == "0":
                with open(args.wordlist, encoding='utf-8') as fh:
                    min_dict = MinDict(read_file_generator(fh, args.blocksize))
                    tarjan = min_dict.tarjan
                continue

            if choice == "1":
                word = input(MESSAGES[language]["wordinput"])
                import time
                # fh = open(args.wordlist)
                now = time.time()
                if tarjan.is_in_language(word):
                    print(f"\n\033[92m\"{word}\"\033[0m " + MESSAGES[language]["wordInLang"] + "\n")
                else:
                    print(f"\n\033[91m\"{word}\"\033[0m " + MESSAGES[language]["wordNotInLang"] + "\n")
                print("took {}".format(time.time()-now))

                # now = time.time()
                # print(find_in_file(fh, word))
                # print("filesearch took {}".format(time.time()-now))

                continue

            if choice == "2":
                figure = draw_automaton(min_dict)
                figure.render('graphviz/aut.gv', view=True)
                print("\n\033[96m" + MESSAGES[language]["saved"] + "\033[0m\n")
                continue

            if choice == "3" :
                save(tarjan, args.filename)
                print("\n\033[96m" + MESSAGES[language]["automaton_saved"] + "\033[0m\n")
                continue

            if choice == "4" :
                tarjan = load(tarjan, args.filename)
                print("\n\033[96m" + MESSAGES[language]["automaton_loaded"] + "\033[0m\n")
                continue

            if choice == "X" :
                print(MESSAGES[language]["bye"])
                break

        print("\n\033[91m" + MESSAGES[language]["warning"] + "\033[0m\n")



if __name__ == "__main__":
    main()

