#!/usr/bin/python3 -u
"""
Entry file for the MinDict Implementation.
"""

from argparse import ArgumentParser,RawTextHelpFormatter,ArgumentDefaultsHelpFormatter
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
        lines.append(line.rstrip())
        if len(lines) == blocksize:
            yield lines
            lines = []
    yield lines


def main():
    """
    Central user interface.
    """

    description = """
    Minimaler Lexikonautomat, Basismodul CL WS 20/21
    
    Authors:
        Philipp Koch
        Pascal Guldener
    
    Erweiterungen
        Grafische Darstellung
        Speichern/Laden
            nur die Tarjan-Tabelle wird gespeichert
        Tarjan-Tabelle 
            wird bei der Konstruktion berechnet und für die Überprüfung der Zugehörigkeit 
            von Wörtern zur Sprache des Automaten verwendet
    
    """
    # Parse arguments
    parser = ArgumentParser(description=description,
                                 formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-wl",
        "--wordlist",
        type=str,
        default="wordlist.txt",
        help="Path to the sorted wordlist (default: %(default)s)")
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        default="automaton.pkl",
        help="Filename for saving/loading automaton (default: %(default)s)")
    parser.add_argument(
        "-cs",
        "--chunksize",
        type=int,
        default=100,
        help="Chunksize in lines from wordlist (default: %(default)s)")
    args = parser.parse_args()

    min_dict = None
    tarjan = None

    # interact with the user
    language = "de"
    allowed_options = set(["X", ""])
    while True:
        try:
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
                        min_dict = MinDict(read_file_generator(fh, args.chunksize))
                        tarjan = min_dict.tarjan
                    continue

                if choice == "1":
                    word = input(MESSAGES[language]["wordinput"])
                    if (len(word) == 0):
                        choice = "X"
                    else:
                        if tarjan.is_in_language(word):
                            print(f"\n\033[92m\"{word}\"\033[0m " + MESSAGES[language]["wordInLang"] + "\n")
                        else:
                            print(f"\n\033[91m\"{word}\"\033[0m " + MESSAGES[language]["wordNotInLang"] + "\n")
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

                if choice == "X" or choice == "" :
                    print(MESSAGES[language]["bye"])
                    break
        except Exception as e:
            print("\n\033[91m" + MESSAGES[language]["error"] + "\033[0m\n")
            print(e)
            continue

        print("\n\033[91m" + MESSAGES[language]["warning"] + "\033[0m\n")
        print('\r', flush=True)



if __name__ == "__main__":
    main()

