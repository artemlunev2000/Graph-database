from src.grammar import Grammar


def analise(script):
    grammar = Grammar()
    gr = grammar.read_grammar('db_grammar.txt')
    return Grammar.cyk(gr, script.replace(' ', '').replace('\n', ''))
