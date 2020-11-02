from src.graph import Graph
from src.grammar import Grammar
from pygraphblas import Matrix, BOOL


def test_cyk_1():
    grammar1 = Grammar()
    gr = grammar1.read_grammar("tests/test_data/grammars/grammar1.txt")

    assert Grammar.cyk(gr, 'ab')
    assert Grammar.cyk(gr, 'acdb')
    assert Grammar.cyk(gr, '')
    assert not Grammar.cyk(gr, 'acdbab')


def test_cyk_2():
    grammar2 = Grammar()
    gr = grammar2.read_grammar("tests/test_data/grammars/grammar2.txt")

    assert Grammar.cyk(gr, 'ab')
    assert not Grammar.cyk(gr, '')
    assert not Grammar.cyk(gr, 'a')
    assert not Grammar.cyk(gr, 'b')


def test_hellings_1():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar1.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph1.txt')

    matrix = Grammar.hellings_algo(gr, graph)

    expected = Matrix.sparse(BOOL, 4, 4)

    expected[0, 1] = True
    expected[0, 2] = True
    expected[1, 2] = True
    expected[3, 0] = True
    expected[3, 1] = True

    assert expected.iseq(matrix)

def test_hellings_2():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar2.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph2.txt')

    matrix = Grammar.hellings_algo(gr, graph)

    expected = Matrix.sparse(BOOL, 5, 5)

    expected[0, 2] = True
    expected[2, 2] = True
    expected[2, 4] = True

    assert expected.iseq(matrix)

def test_hellings_3():
    grammar = Grammar()
    gr = grammar.read_grammar("tests/test_data/cfpq/cfpq_grammar3.txt")

    graph = Graph()
    graph.read_graph('tests/test_data/cfpq/cfpq_graph3.txt')

    matrix = Grammar.hellings_algo(gr, graph)

    expected = Matrix.sparse(BOOL, 3, 3)

    expected[0, 0] = True
    expected[1, 1] = True
    expected[2, 2] = True
    expected[1, 2] = True

    assert expected.iseq(matrix)
