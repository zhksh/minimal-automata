from typing import Dict
class Tarjantable():
    def __init__(self, trie=None) -> None:
        self.tt = [None]
        self.last_slot = 0
        if trie is not None:
            mostright_state = trie.find_last_state()
            self.store_state(mostright_state, trie.transitions, mostright_state in trie.final_states)
            parents = trie.parents_of([mostright_state])
            while len(parents) > 0:
                for parent_id in parents:
                    self.store_state(parent_id, trie.transitions, parent_id in trie.final_states)
                parents = trie.parents_of(parents)




    def find_slot(self, state: int,transitions: Dict[int, Dict[str, int]]) -> int:
        slot = self.last_slot
        while True:
            found = True
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

        while not self.last_slot >= len(self.tt) and self.tt[self.last_slot] is not None: self.last_slot += 1

        return state_slot


    def index_of(self, state_id) -> int:
        for i, cell in enumerate(self.tt,0):
            if cell is not None and cell[1] == 'state' and cell[0] == state_id: return i

        raise Exception("implementation err: {} was not found".format(state_id))


    def alloc_check_cell(self,slot, char) -> bool:
        next_index = slot + ord(char)
        if next_index > len(self.tt):
            self.tt.extend([None]*(next_index-len(self.tt)+1))
            return True
        return self.tt[next_index] is None
