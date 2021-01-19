usage: main.py [-h] [-wl WORDLIST] [-f FILENAME] [-cs CHUNKSIZE]

    Minimaler Lexikonautomat, Basismodul CL WS 20/21
    Authors:
        Philipp Koch
        Pascal Guldener
    
    Erweiterungen
        Grafische Darstellung
        Speichern/Laden
            nur die Tarjan-Tabelle wird gespeichert
        Tarjan-Tabelle 
            wird bei der Konstruktion berechnet für die Überprüfung der Zugehörigkeit 
            von Wörtern zur Sprache des Automaten verwendet
    
    

optional arguments:
  -h, --help            show this help message and exit
  -wl WORDLIST, --wordlist WORDLIST
                        Path to the sorted wordlist (default: wordlist.txt)
  -f FILENAME, --filename FILENAME
                        Filename for saving/loading automaton (default: automaton.pkl)
  -cs CHUNKSIZE, --chunksize CHUNKSIZE
                        Chunksize in lines from wordlist (default: 100)
