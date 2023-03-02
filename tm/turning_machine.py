from typing import Union, List

class State:
    
    def __init__(self, tm: TuringMachine, name: str=None) -> None:
        self.name = f"q_{tm.num_states}"
        tm.num_states += 1
        self.
        
        
class Transition:
    
    def __init__(self, source: State, dest: State, tape_read: str, tape_write: str, tape_direction: Union[int, str]) -> None:
        self.qi = source
        self.qj = dest
        
        self.tr = tape_read
        self.tw = tape_write
        self.td = tape_direction
        
        assert tape_direction == -1 or tape_direction == 1 or tape_direction == "L" or tape_direction == "R", "Tape Direction must either be L, R, -1, or 1"
        
        
    def get_source(self) -> State:
        return self.qi
        
    def get_dest(self) -> State:
        return self.qj
        
class Tape:
    
    def __init__(self, w: str=""):
        self.__tape = w
        self.pointer = 0
        
    def __getitem__(self, idx):
        assert idx >= 0 and type(idx) == int, "Idx must be a non-negative integer"
        if idx < len(self.__tape):
            return self.__tape[idx]
        else:
            return "_"
            
    def __setitem__(self, idx)
        pass
    
class TuringMachine:
    
    def __init__(self, states: List[State]=None, num_states: int=0) -> None:
        self.num_states = 0
        if states is None and num_states == 0:
            self.Q = [State(tm=self) for _ in range(num_states)]
        else:
            self.Q = states
            self.num_states = len(states)
            
        self.transitions = {}
        
        
        
        
        