from src.graph import Graph
from src.grammar import Grammar
from pygraphblas import Matrix, BOOL


def test_tensor_1():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar1.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph1.txt')

    matrix = Grammar.cfpq_tensor(gr, graph)

    expected = Matrix.sparse(BOOL, 5, 5)

    expected[0, 2] = True
    expected[2, 2] = True
    expected[2, 4] = True

    assert expected.iseq(matrix)


def test_tensor_2():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar2.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph2.txt')

    matrix = Grammar.cfpq_tensor(gr, graph)

    expected = Matrix.sparse(BOOL, 3, 3)

    expected[0, 0] = True
    expected[1, 1] = True
    expected[2, 2] = True
    expected[1, 2] = True

    assert expected.iseq(matrix)


def test_mul_1():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar1.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph1.txt')

    matrix = Grammar.cfpq_multiplication(gr, graph)

    expected = Matrix.sparse(BOOL, 5, 5)

    expected[0, 2] = True
    expected[2, 2] = True
    expected[2, 4] = True

    assert expected.iseq(matrix)


def test_mul_2():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar2.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph2.txt')

    matrix = Grammar.cfpq_multiplication(gr, graph)

    expected = Matrix.sparse(BOOL, 3, 3)

    expected[0, 0] = True
    expected[1, 1] = True
    expected[2, 2] = True
    expected[1, 2] = True

    assert expected.iseq(matrix)
