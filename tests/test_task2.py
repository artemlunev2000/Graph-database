from src.graph import Graph
from pygraphblas import Matrix, BOOL


def test_intersection():
    graph1 = Graph()
    graph1.read_graph('tests/test_data/graph1.txt')
    regex1 = Graph()
    regex1.read_regex('tests/test_data/regex1.txt')

    intersection = graph1.intersect(regex1)

    assert intersection.projection_matrices['a'].nvals == 1
    assert intersection.projection_matrices['b'].nvals == 1
    assert intersection.projection_matrices['c'].nvals == 2


def test_empty_intersection():
    graph2 = Graph()
    graph2.read_graph('tests/test_data/graph2.txt')
    regex2 = Graph()
    regex2.read_regex('tests/test_data/regex2.txt')

    intersection = graph2.intersect(regex2)

    assert len(intersection.projection_matrices.keys()) == 0


def test_reachable_with_start_states():
    graph3 = Graph()
    graph3.read_graph('tests/test_data/graph3.txt')

    result = graph3.reachable_with_start_states([1, 2])
    expected = Matrix.sparse(BOOL, graph3.size, graph3.size)

    expected[1, 2] = True
    expected[1, 3] = True
    expected[2, 3] = True

    assert expected.iseq(result)


def test_reachable_with_start_and_final_states():
    graph3 = Graph()
    graph3.read_graph('tests/test_data/graph3.txt')

    result = graph3.reachable_with_start_and_final_states([1], [2])
    expected = Matrix.sparse(BOOL, graph3.size, graph3.size)

    expected[1, 2] = True

    assert expected.iseq(result)
