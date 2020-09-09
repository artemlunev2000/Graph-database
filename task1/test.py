from pyformlang.finite_automaton import EpsilonNFA, State, Symbol
from pygraphblas import Matrix


def test_nfa_intersection():
    enfa1 = EpsilonNFA()
    enfa2 = EpsilonNFA()

    state0 = State(0)
    state1 = State(1)
    state2 = State(2)

    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")

    enfa1.add_start_state(state0)
    enfa1.add_final_state(state2)
    enfa1.add_transitions([
        (state0, symb_a, state1),
        (state1, symb_a, state2),
        (state1, symb_b, state2)])

    enfa2.add_start_state(state0)
    enfa2.add_final_state(state2)
    enfa2.add_transitions([
        (state0, symb_a, state1),
        (state1, symb_a, state2),
        (state1, symb_c, state2)])

    expected = EpsilonNFA()
    expected.add_start_state(state0)
    expected.add_final_state(state2)
    expected.add_transitions([
        (state0, symb_a, state1),
        (state1, symb_a, state2)])

    result = enfa1.get_intersection(enfa2)

    assert expected.is_equivalent_to(result)


def test_matrix_multiplication():
    matrix_a = Matrix.from_lists(
        [0, 1, 2],
        [1, 2, 0],
        [1, 4, 2])

    matrix_b = Matrix.from_lists(
        [0, 1, 2],
        [1, 2, 0],
        [3, 2, 1])

    matrix_expected = Matrix.from_lists(
        [0, 1, 2],
        [2, 0, 1],
        [2, 4, 6])

    matrix_result = matrix_a @ matrix_b

    assert matrix_expected.iseq(matrix_result)
