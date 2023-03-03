from typing import Union, List


class State:
    def __init__(
        self, tm, name: str = None, accepting: bool = False, rejecting: bool = False
    ) -> None:
        self.name = f"q{tm.num_states}" if name is None else name
        tm.num_states += 1
        self.tm = tm
        self.accepting = accepting
        self.rejecting = rejecting

    def final(self):
        return self.accepting or self.rejecting


class Transition:
    def __init__(
        self,
        source: State,
        dest: State,
        tape_read: str,
        tape_write: str,
        tape_direction: Union[int, str],
    ) -> None:
        self.qi = source
        self.qj = dest

        self.tr = tape_read
        self.tw = tape_write
        self.td = tape_direction

        assert (
            tape_direction == -1
            or tape_direction == 1
            or tape_direction == "L"
            or tape_direction == "R"
        ), "Tape Direction must either be L, R, -1, or 1"

    def get_source(self) -> State:
        return self.qi

    def get_dest(self) -> State:
        return self.qj


class Tape:
    directions_map = {
        "R": 1,
        "L": -1,
        1: 1,
        -1: -1,
    }

    def __init__(self, w: str = "", tape_alphabet=set("ab_")):
        self.__tape = list(w)
        self.pointer = 0
        self.gamma = tape_alphabet

    def __getitem__(self, idx):
        assert idx >= 0 and type(idx) == int, "Idx must be a non-negative integer"
        if idx < len(self.__tape):
            return self.__tape[idx]
        else:
            return "_"

    def __setitem__(self, idx, val):
        assert idx >= 0 and type(idx) == int, "Idx must be a non-negative integer"
        assert (
            type(val) == str and len(val) == 1
        ), "Value must be a single character string"
        assert val in self.gamma, "Value must be in tape alphabet"
        if idx >= len(self.__tape):
            self.__tape = self.__tape + ["_"] * (idx + 1 - len(self.__tape))
        self.__tape[idx] = val

    def read(self):
        return self[self.pointer]

    def write(self, val):
        self[self.pointer] = val

    def move(self, direction):
        direction = Tape.directions_map[direction]
        self.pointer = max(0, self.pointer + direction)

    def get_tape_str(self):
        return "".join(self.__tape)

    def snapshot(self):
        tape_str = self.get_tape_str()
        return tape_str[: self.pointer] + ">" + tape_str[self.pointer :]


class TuringMachine:
    def __init__(
        self,
        start_state: State = None,
        states: List[State] = None,
        num_states: int = 0,
        input_alphabet: set = set("ab"),
        tape_alphabet: set = set(),
    ) -> None:
        self.num_states = 0
        if states is None:
            self.Q = [State(tm=self) for _ in range(num_states)]
            self.q0 = self.Q[0]
        else:
            self.Q = states
            self.num_states = len(states)
            if start_state is None:
                self.q0 = self.Q[0]
            else:
                self.q0 = start_state
                assert self.q0 in self.Q, "Start state must be in states list"

        assert "_" not in input_alphabet, "Input alphabet cannot include _"

        self.delta = {}
        self.sigma = input_alphabet
        self.gamma = input_alphabet.union(tape_alphabet)
        self.gamma.add("_")

        self.Q_dict = {s.name: s for s in self.Q}

    def get_state(self, key: Union[str, int]):
        if type(key) == int:
            if f"q{key}" in self.Q_dict:
                key = f"q{key}"
            else:
                if key >= len(self.Q):
                    raise Exception("Invalid state key")
                key = self.Q[key].name

        return self.Q_dict[key]

    def mark_final_state(self, key: Union[str, int], accept: bool = True):
        if accept:
            self.get_state(key=key).accepting = True
            self.get_state(key=key).rejecting = False
        else:
            self.get_state(key=key).accepting = False
            self.get_state(key=key).rejecting = True

    def add_transition(self, qi, qj, tr, tw, td):
        qi = self.get_state(qi)
        qj = self.get_state(qj)
        self.delta[(qi, tr)] = Transition(
            source=qi, dest=qj, tape_read=tr, tape_write=tw, tape_direction=td
        )

    def add_transitions(self, trans_args):
        [self.add_transition(*args) for args in trans_args]

    def apply_transition(self, tape, trans):
        tape.write(trans.tw)
        tape.move(trans.td)
        return trans.get_dest()

    def create_snapshot(self, tape: Tape, q: State):
        return tape.snapshot().replace(">", f"[{q.name}>]")

    def normalize_snapshots(self, snapshots):
        max_len = max([len(s) for s in snapshots]) + 2
        return [snap + "_" * (max_len - len(snap)) for snap in snapshots]

    def compute(self, w: str = ""):
        for c in w:
            assert c in self.sigma, "Characters must be in input alphabet"
        tape = Tape(w=w, tape_alphabet=self.gamma)
        q = self.q0
        snapshots = []
        snapshots.append(self.create_snapshot(tape, q))
        while not q.final():
            k = (q, tape.read())
            if k not in self.delta:
                break
            q = self.apply_transition(tape, self.delta[k])
            snapshots.append(self.create_snapshot(tape, q))
        snapshots = self.normalize_snapshots(snapshots)
        return tape.get_tape_str().rstrip("_"), q.accepting, snapshots
