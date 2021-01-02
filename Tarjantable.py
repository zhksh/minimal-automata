from typing import Dict

class Tarjantable():
    """This is a Tarjantable implementation """

    def __init__(self) -> None:
        self.tt = [None]
        self.last_slot = 0
        self.init_state = -1
        self.trans_cell_desc = "trans"
        self.state_cell_desc = "state"


    def find_slot(self, state: int, transitions) -> int:
        """we need to find an index that is free and has free offsets for each transition"""

        slot = self.last_slot
        while True:
            success = True
            for label, s in transitions.items():
                if not self.is_empty_or_alloc(slot, label):
                   success = False
                   slot += 1
                   break
            if success: return slot
            while self.tt[slot] is not None:
                slot += 1
        return slot


    def store_state(self, state: int, transitions: Dict[str, int], is_final: bool, is_init=False) -> int:
        """populate the array, a cell is a simple tuple .
         the original state_id is left only for debugging purposes"""
        state_slot = self.find_slot(state, transitions)
        self.tt[state_slot] = (self.state_cell_desc, state, is_final)
        for label, right_state in transitions.items():
            self.tt[state_slot + ord(label)] = (self.trans_cell_desc, label, self.index_of(right_state))
        self.inc_last_slot()
        if is_init: self.init_state = state_slot
        return state_slot


    def inc_last_slot(self):
        while not self.last_slot >= len(self.tt) and self.tt[self.last_slot] is not None:
            self.last_slot += 1


    def index_of(self, state) -> int:
        """find the index of a previously added state, this is only used for construction,
        after that state stateids and indexes are consistent"""

        for i, cell in enumerate(self.tt,0):
            if cell is not None and cell[0] == self.state_cell_desc  and cell[1] == state:
                return i

        return -1


    def is_empty_or_alloc(self, slot, char) -> bool:
        """before inserting new elements the array needs to be checked and adjusted for length and the cell for emptyness"""

        next_index = slot + ord(char)
        if next_index >= len(self.tt):
            self.tt.extend([None]*(next_index-len(self.tt)+1))
            return True
        return self.tt[next_index] is None


    def lookup(self, label, state) -> tuple:
        """look for the contents of a cell"""
        position = ord(label)
        if position + state > len(self.tt): return None

        return self.tt[state+position]


    def is_in_language(self, word) -> bool:
        state = self.init_state
        for c in word:
            transition = self.lookup(c, state)
            if transition is not None \
                    and transition[0] == self.trans_cell_desc \
                    and transition[1] == c:
                state = transition[2]
            else:
                return False

        return True
