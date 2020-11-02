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

        pairs = []
        units = []

        if grammar.generate_epsilon():
            matrix = Matrix.sparse(BOOL, graph.size, graph.size)
            for i in range(graph.size):
                matrix[i, i] = True
                deq.append((grammar.start_symbol, i, i))
            result[grammar.start_symbol] = matrix

        cfg_normal = grammar.to_normal_form()

        for prod in cfg_normal.productions:
            if len(prod.body) == 2:
                pairs.append(prod)
            if len(prod.body) == 1:
                units.append(prod)

        for t, matrix in graph.projection_matrices.items():
            for prod in units:
                if prod.body == [Terminal(t)]:
                    if prod.head not in result:
                        result[prod.head] = matrix.dup()
                    else:
                        result[prod.head] += matrix.dup()

        for var, matrix in result.items():
            for i, j, _ in zip(*matrix.to_lists()):
                deq.append((var, i, j))

        while deq:
            res_list = list()
            var, v_start, v_end = deq.popleft()

            for new_var, matrix in result.items():
                for new_from, _ in matrix[:, v_start]:
                    for prod in pairs:
                        if (prod.body[0] == new_var and prod.body[1] == var and len(prod.body) == 2 and
                                (prod.head not in result or result[prod.head].get(new_from, v_end) is None)):
                            deq.append((prod.head, new_from, v_end))
                            res_list.append((prod.head, new_from, v_end))

            for new_var, matrix in result.items():
                for new_start, _ in matrix[v_end, :]:
                    for prod in pairs:
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

    def cfpq_multiplication(grammar: CFG, graph: Graph):
        res = dict()
        res[grammar.start_symbol] = Matrix.sparse(BOOL, graph.size, graph.size)

        if grammar.generate_epsilon():
            for i in range(graph.size):
                res[grammar.start_symbol][i, i] = True

        cfg = grammar.to_normal_form()

        pairs = []
        units = []
        for prod in cfg.productions:
            if len(prod.body) == 2:
                pairs.append(prod)
            if len(prod.body) == 1:
                units.append(prod)

        for label, matrix in graph.projection_matrices.items():
            for prod in units:
                if Terminal(label) == prod.body[0]:
                    if prod.head in res:
                        res[prod.head] += matrix
                    else:
                        res[prod.head] = matrix

        is_changed = True
        while is_changed:
            is_changed = False
            for prod in pairs:
                if prod.body[0] in res and prod.body[1] in res:
                    if prod.head not in res:
                        res[prod.head] = Matrix.sparse(BOOL, graph.size, graph.size)
                    prev = res[prod.head].nvals
                    res[prod.head] += res[prod.body[0]] @ res[prod.body[1]]
                    is_changed = prev != res[prod.head].nvals

        return res[cfg.start_symbol]

    def to_recursive(grammar: CFG):
        rsm = Graph()
        heads = dict()

        rsm.size = sum([len(prod.body) + 1 for prod in grammar.productions])
        rsm.vertices = set(range(rsm.size))
        i = 0
        for prod in grammar.productions:
            start_state = i
            final_state = i + len(prod.body)

            rsm.start_vertices.add(start_state)
            rsm.final_vertices.add(final_state)
            heads[(start_state, final_state)] = prod.head.value

            for var in prod.body:
                matrix = rsm.projection_matrices.get(var.value, Matrix.sparse(
                    BOOL, rsm.size, rsm.size))

                matrix[i, i + 1] = True
                rsm.labels.add(var.value)
                rsm.projection_matrices[var.value] = matrix
                i += 1

            i += 1

        return rsm, heads

    def cfpq_tensor(grammar: CFG, graph: Graph):
        rsm, heads = Grammar.to_recursive(grammar)

        rsm.size = sum([len(prod.body) + 1 for prod in grammar.productions])
        rsm.vertices = set(range(rsm.size))
        i = 0
        for prod in grammar.productions:
            start_state = i
            final_state = i + len(prod.body)

            rsm.start_vertices.add(start_state)
            rsm.final_vertices.add(final_state)
            heads[(start_state, final_state)] = prod.head.value

            for var in prod.body:
                matrix = rsm.projection_matrices.get(var.value, Matrix.sparse(BOOL, rsm.size, rsm.size))
                matrix[i, i + 1] = True
                rsm.labels.add(var.value)
                rsm.projection_matrices[var.value] = matrix
                i += 1

            i += 1

        for prod in grammar.productions:
            if len(prod.body) == 0:
                matrix = Matrix.sparse(BOOL, graph.size, graph.size)

                for i in range(graph.size):
                    matrix[i, i] = True
                graph.labels.add(prod.head)
                graph.projection_matrices[prod.head] = matrix

        is_changed = True
        while is_changed:
            is_changed = False
            intersection = rsm.intersect(graph)
            closure = intersection.transitive_closure_square()

            for i, j, k in zip(*closure.to_lists()):
                rfa_from, rfa_to = i // graph.size, j // graph.size
                graph_from, graph_to = i % graph.size, j % graph.size

                if (rfa_from, rfa_to) not in heads:
                    continue
                var = heads[(rfa_from, rfa_to)]

                matrix = graph.projection_matrices.get(var, Matrix.sparse(BOOL, graph.size, graph.size))

                if matrix.get(graph_from, graph_to) is None:
                    is_changed = True
                    matrix[graph_from, graph_to] = True
                    graph.labels.add(var)
                    graph.projection_matrices[var] = matrix

        return graph.projection_matrices[grammar.start_symbol]
