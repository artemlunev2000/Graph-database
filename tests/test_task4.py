from src.graph import Graph
from src.grammar import Grammar
from pygraphblas import Matrix, BOOL


def test_cyk_1():
    grammar1 = Grammar()
    gr = grammar1.read_grammar("tests/test_data/grammar1.txt")

    assert Grammar.cyk(gr, 'ab')
    assert Grammar.cyk(gr, 'acdb')
    assert Grammar.cyk(gr, '')
    assert not Grammar.cyk(gr, 'acdbab')


def test_cyk_2():
    grammar2 = Grammar()
    gr = grammar2.read_grammar("tests/test_data/grammar2.txt")

    assert Grammar.cyk(gr, 'ab')
    assert not Grammar.cyk(gr, '')
    assert not Grammar.cyk(gr, 'a')
    assert not Grammar.cyk(gr, 'b')


def test_hellings():
    grammar3 = Grammar()
    gr = grammar3.read_grammar("tests/test_data/grammar3.txt")

    graph4 = Graph()
    graph4.read_graph('tests/test_data/graph4.txt')

    matrix = Grammar.hellings_algo(gr, graph4)

    expected = Matrix.sparse(BOOL, 4, 4)

    expected[0, 1] = True
    expected[0, 2] = True
    expected[1, 2] = True
    expected[3, 0] = True
    expected[3, 1] = True
    expected[3, 2] = True

    assert expected.iseq(matrix)
