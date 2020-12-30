from typing import Dict

class Tarjantable():

    def __init__(self, trie=None) -> None:
        self.tt = [None]
        self.last_slot = 0
        if trie is not None:
            self.trie = trie
            mostright_state = trie.find_last_state()
            self.store_state(mostright_state, None, None, mostright_state in trie.final_states)
            self.postorder_iterate(mostright_state)


    def postorder_iterate(self, child_state: int) -> None:
        # self.store_state(child_state, label, self.trie.transitions[child_state], child_state in self.trie.final_states)
        parent_states = self.trie.parents_of([child_state])
        if len(parent_states) == 0: return
        for label, parent_state in parent_states:
            self.store_state(parent_state, label, child_state, parent_state in self.trie.final_states)
            self.postorder_iterate(parent_state)

        return


    def find_slot(self, state: int) -> int:
        slot = self.last_slot
        while True:
            success = True
            for label, s in self.trie.transitions[state].items():
                if not self.is_empty_or_alloc(slot, label):
                   success = False
                   slot += 1
                   break
            if success: return slot
            while self.tt[slot] is not None: slot += 1
        return slot



    def store_state(self, state: int,label: str, child_state: int, is_final: bool) -> int:
        state_idx = self.index_of(state)
        if state_idx == -1:
            state_slot = self.find_slot(state)
            self.tt[state_slot] = (state, "state", is_final)
        else:
            last_slot_tmp = self.last_slot
            self.last_slot = state_idx
            state_slot = self.find_slot(state)
            self.last_slot = last_slot_tmp

        # for label, s in transitions.items():
        if label is not None:
            self.tt[state_slot + ord(label)] = ("trans", label, self.index_of(child_state))

        while not self.last_slot >= len(self.tt) and self.tt[self.last_slot] is not None: self.last_slot += 1

        return state_slot


    def index_of(self, state) -> int:
        for i, cell in enumerate(self.tt,0):
            if cell is not None and cell[1] == 'state' and cell[0] == state: return i

        return -1


    def is_empty_or_alloc(self, slot, char) -> bool:
        next_index = slot + ord(char)
        if next_index >= len(self.tt):
            self.tt.extend([None]*(next_index-len(self.tt)+1))
            return True
        return self.tt[next_index] is None
