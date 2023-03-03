import sys

from .turning_machine import TuringMachine

show_config = len(sys.argv) > 1


def run(tm, inp):
    tape, accept, configs = tm.compute(inp)
    print(inp, "-->", tape, accept)

    if show_config:
        print("--------------------------------")
        for config in configs:
            print(config)

    return tape, accept, configs


def bit_flip():
    tm = TuringMachine(num_states=2)
    tm.add_transitions(
        [(0, 0, "a", "b", "R"), (0, 0, "b", "a", "R"), (0, 1, "_", "_", "L")]
    )
    tm.mark_final_state(1)

    inp = "aba"

    run(tm, inp)


def copy_str():
    tm = TuringMachine(num_states=5, input_alphabet=set("ab#"), tape_alphabet=set("01"))
    tm.add_transitions(
        [
            (0, 1, "a", "0", "R"),
            (1, 1, "a", "a", "R"),
            (1, 1, "a", "a", "R"),
            (1, 1, "b", "b", "R"),
            (1, 1, "#", "#", "R"),
            (1, 2, "_", "a", "L"),
            (2, 2, "a", "a", "L"),
            (2, 2, "b", "b", "L"),
            (2, 2, "#", "#", "L"),
            (2, 0, "0", "a", "R"),
            (2, 0, "1", "b", "R"),
            (0, 3, "b", "1", "R"),
            (3, 3, "a", "a", "R"),
            (3, 3, "b", "b", "R"),
            (3, 3, "#", "#", "R"),
            (3, 2, "_", "b", "L"),
            (0, 4, "#", "#", "R"),
        ]
    )
    tm.mark_final_state(4)

    inp = "aba#"
    run(tm, inp)


def index_array():
    b = set("ab")
    N = 10
    a = set([str(i) for i in range(N + 1)])
    l = set([str(i + 1) for i in range(N + 1)])
    s = b.union(a)
    s.add("#")

    tm = TuringMachine(num_states=11, input_alphabet=s)

    tm.add_transitions(
        [(0, 1, k, str(int(k) - 1), "R") for k in l]
        + [(1, 1, k, "_", "R") for k in b]
        + [(1, 1, "_", "_", "R")]
        + [(1, 2, "#", "_", "L"), (2, 2, "_", "_", "L")]
        + [(2, 1, k, str(int(k) - 1), "R") for k in l]
        + [(0, 3, "0", "0", "R"), (2, 3, "0", "0", "R"), (3, 3, "_", "_", "R")]
        + [(3, 4, k, k, "R") for k in b]
        + [(4, 4, k, k, "R") for k in b]
        + [
            (4, 5, "#", "#", "L"),
            (4, 5, "_", "#", "L"),
            (5, 6, "a", "#", "L"),
            (5, 7, "b", "#", "L"),
            (6, 6, "a", "a", "L"),
            (7, 7, "b", "b", "L"),
            (6, 7, "b", "a", "L"),
            (7, 6, "a", "b", "L"),
            (6, 4, "_", "a", "R"),
            (7, 4, "_", "b", "R"),
            (6, 8, "0", "a", "R"),
            (7, 8, "0", "b", "R"),
            (6, 8, "0", "a", "R"),
        ]
        + [(8, 8, k, k, "R") for k in b]
        + [(8, 9, "#", "_", "R") for k in b]
        + [(9, 9, k, "_", "R") for k in s]
        + [(9, 10, "_", "_", "R")]
    )

    tm.mark_final_state(10)

    def create_inp(A, i):
        return str(i) + "#".join(A)

    A = ["aabaaa", "abbaa", "bba", "aab", "aaa"]
    i = 0

    inp = create_inp(A, i)
    tape, _, _ = run(tm, inp)

    print("tape == A[i] is", tape == A[i])


if __name__ == "__main__":
    index_array()
