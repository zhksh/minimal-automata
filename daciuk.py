"""
MinDict Implementation für das Basismodul im Master Computerlinguistik.
"""
from itertools import count
from collections import OrderedDict
from Tarjantable import Tarjantable



class MinDict:
    """
    Konstruktion  eines  minimierten  Automaten  anhandeiner sortierten Wortliste
    """
    def __init__(self, data_generator):
        self.final_states = set()
        self.curr_id = count()
        self.transitions = dict()
        self.initial_state = 0
        self.tarjan = Tarjantable()

        next(self.curr_id)

        self.compile(data_generator)


    def compile(self, data_generator) -> None:
        """
        Method for compilation of the automaton
        """
        read = 0
        for words in data_generator:
            for word in words:
                common_prefix, split_state = self.commonprefix(word)
                curr_suffix = word[len(common_prefix)::]

                if len(self.transitions[split_state]) > 0:
                    self.replace_or_register(split_state)

                self.add_suffix(curr_suffix, split_state)
            read += len(words)
            print("read {} {}".format(read, "\r"), flush=True)
        if len(self.transitions) == 0:
            self.transitions[self.initial_state] = OrderedDict()
        self.replace_or_register(self.initial_state)
        self.tarjan.store_state(self.initial_state,
                                    self.transitions[self.initial_state],
                                    False,
                                    is_init=True)


    def replace_or_register(self, state) -> None:
        """
        Method for replacing superflous states.
        """

        last_child = next(reversed(self.transitions[state].items()))
        last_child_label, last_child_state = last_child[0], last_child[1]

        if self.has_children(last_child_state):
            self.replace_or_register(last_child_state)

        equivalency, state_subst = self.equivalent(last_child_state)
        if equivalency:
            self.transitions[state][last_child_label] = state_subst
            if last_child_state in self.final_states:
                self.final_states.remove(last_child_state)
            del self.transitions[last_child_state]
        else:
            self.tarjan.store_state(last_child_state,
                                    self.transitions[last_child_state],
                                    last_child_state in self.final_states)


    def equivalent(self, left_state) -> bool:
        """
        Check if there exists another equivalent state in the automaton.
        """
        for right_state in self.transitions:
            if right_state == left_state:
                continue
            final = (left_state in self.final_states) == (right_state in self.final_states)
            outgoing = self.transitions[left_state] == self.transitions[right_state]
            if final and outgoing:
                return True, right_state
        return False, None


    def has_children(self, state) -> bool:
        """
        Check if the state has children states.
        """
        return len(self.transitions[state]) > 0


    def commonprefix(self, word) -> (str, int):
        """
        Method to obtain the longest common prefix of a new word and the already stored words.
        """
        curr = 0
        index = 0
        if 0 not in self.transitions:
            self.transitions[0] = OrderedDict()
        while index < len(word):
            if not word[index] in self.transitions[curr]:
                break
            curr = self.transitions[curr][word[index]]
            index -=- 1
        return word[:index], curr


    def add_suffix(self, suffix, state) -> None:
        """
        Method to add the suffix to the automaton.
        """
        for char in suffix:
            next_state = next(self.curr_id)
            if state in self.transitions:
                self.transitions[state][char] = next_state
            else:
                self.transitions[state] = OrderedDict()
                self.transitions[state][char] = next_state
            # if self.tarjan is not None:
            #     self.tarjan.store_state(state, self.transitions[state], state in self.final_states)
            state = next_state
        self.transitions[state] = OrderedDict()
        self.final_states.add(state)


    def is_in_dict(self, word) -> bool:
        """
        Method to check wether a word is in the dict or not.
        """
        state = self.initial_state
        for char in word:
            if char not in self.transitions[state]:
                return False
            state = self.transitions[state][char]
        if state in self.final_states:
            return True
        return False


    def is_in_tarjan_table(self, word) -> bool:
        """
        Method to check wether a word is in the dict or not using the constructed Tarjan table, we could actually
        throw away the transitions now.
        """
        return self.tarjan.is_in_language(word)

    ## PROPERTIES ##

    @property
    def states(self):
        """states property for display purpose"""
        return self.transitions.keys()

    @property
    def delta(self):
        """delta property for display purpose"""
        delta_list = []
        for key, values in self.transitions.items():
            delta_list = (
                delta_list +
                list(map(lambda x, keylamb=key : (keylamb, x[0], x[1]), list(values.items())))
                )
        return delta_list
