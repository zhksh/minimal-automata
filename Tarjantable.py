from typing import Dict
class Tarjantable():
    def __init__(self, trie=None) -> None:
        self.tt = []
        self.last_slot = 0
        if trie is not None:
            parents = trie.parents_of(trie.final_states)
            for state, transitions in trie.transitions.items():
                self.store_state(state, trie.transitions, state in trie.final_states)



    def find_slot(self, state: int,transitions: Dict[int, Dict[str, int]]) -> int:
        slot = self.last_slot
        found = True
        while True:
            for label, s in transitions[state].items():
                if not self.alloc_check_cell(slot, label):
                    found = False
                    break
            if found: return slot
            while self.tt[slot] is not None: slot += 1

        return slot


    def store_state(self, state: int, transitions: Dict[int, Dict[str, int]], is_final: bool) -> int:
        state_slot = self.find_slot(state, transitions)
        self.tt[state_slot] = (state, "state", is_final)
        for label, s in transitions[state].items():
            self.tt[state_slot + ord(label)] = ("trans", label, self.index_of(s))

        while self.tt[self.last_slot] is not None: self.last_slot += 1

        return state_slot


    def index_of(self, state_id) -> int:
        for i, cell in enumerate(self.tt,0):
            if cell is not None and cell[1] == 'state' and cell[0] == state_id: return i

        raise Exception("implementation err: {} was not found".format(state_id))

    def alloc_check_cell(self,slot, char) -> bool:
        next_index = slot + ord(char)
        if next_index > len(self.tt):
            self.tt.extend([None]*(next_index-len(self.tt)))
            return True
        return self.tt[next_index] is None
