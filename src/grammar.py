from pyformlang.cfg import CFG, Terminal
from pygraphblas import Matrix, BOOL, Vector
from src.graph import Graph
from collections import deque


class Grammar:
    def read_grammar(self, path):
        with open(path, 'r') as grammar_file:
            productions = []
            for line in grammar_file:
                production = line.split()
                productions.append(production[0] + " -> " + " ".join(production[1:]))
            cfg = CFG.from_text("\n".join(productions))

        return cfg

    def cyk(cfg: CFG, word: str):
        word_size = len(word)
        if word_size == 0:
            return cfg.generate_epsilon()

        cfg_normal = cfg.to_normal_form()
        matrix = [[set() for i in range(word_size)] for j in range(word_size)]

        for i in range(word_size):
            for production in cfg_normal.productions:
                if production.body == [Terminal(word[i])]:
                    matrix[i][i].add(production.head)

        for i in range(word_size):
            for j in range(word_size - i):
                for k in range(i):
                    first = matrix[j][j + k]
                    second = matrix[j + k + 1][j + i]
                    for production in cfg_normal.productions:
                        if (len(production.body) == 2 and production.body[0] in first and
                                production.body[1] in second):
                            matrix[j][j + i].add(production.head)

        return cfg_normal.start_symbol in matrix[0][word_size - 1]

    def hellings_algo(grammar: CFG, graph: Graph):
        result = dict()
        deq = deque()

        if grammar.generate_epsilon():
            matrix = Matrix.sparse(BOOL, graph.size, graph.size)
            for i in range(graph.size):
                matrix[i, i] = True
                deq.append((grammar.start_symbol, i, i))
            result[grammar.start_symbol] = matrix

        cfg_normal = grammar.to_normal_form()

        for term, matrix in graph.projection_matrices.items():
            for prod in cfg_normal.productions:
                if prod.body == [Terminal(term)]:
                    result[prod.head] = matrix

        for var, matrix in result.items():
            for i, j, _ in zip(*matrix.to_lists()):
                deq.append((var, i, j))

        while deq:
            res_list = list()
            var, v_start, v_end = deq.popleft()

            for new_var, matrix in result.items():
                for new_from, _ in matrix[:, v_start]:
                    for prod in cfg_normal.productions:
                        if (prod.body[0] == new_var and prod.body[1] == var and len(prod.body) == 2 and
                                (prod.head not in result or result[prod.head].get(new_from, v_end) is None)):
                            deq.append((prod.head, new_from, v_end))
                            res_list.append((prod.head, new_from, v_end))

            for new_var, matrix in result.items():
                for new_start, _ in matrix[v_end, :]:
                    for prod in cfg_normal.productions:
                        if (prod.body[0] == var and prod.body[1] == new_var and len(prod.body) == 2 and
                                (prod.head not in result or result[prod.head].get(v_start, new_start) is None)):
                            deq.append((prod.head, v_start, new_start))
                            res_list.append((prod.head, v_start, new_start))

            for var, v_start, v_end in res_list:
                matrix = result.get(var, Matrix.sparse(BOOL, graph.size, graph.size))
                matrix[v_start, v_end] = True
                result[var] = matrix

        return result.get(cfg_normal.start_symbol, Matrix.sparse(
            BOOL, graph.size, graph.size))
