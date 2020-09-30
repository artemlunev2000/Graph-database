from pyformlang.regular_expression import Regex
from pygraphblas import Matrix, BOOL, Vector


class Graph:
    def __init__(self):
        self.size = 0
        self.vertices = set()
        self.start_vertices = set()
        self.final_vertices = set()
        self.labels = set()
        self.projection_matrices = dict()

    def read_graph(self, path):
        with open(path, 'r') as graph_file:
            lines = graph_file.readlines()
            for line in lines:
                edge = line.split(" ")
                v_from = int(edge[0])
                v_to = int(edge[2])
                self.vertices.add(v_from)
                self.vertices.add(v_to)
                self.size = max(self.size, v_from + 1, v_to + 1)

            for line in lines:
                edge = line.split(" ")
                v_from = int(edge[0])
                v_to = int(edge[2])
                label = edge[1]
                if label not in self.labels:
                    self.labels.add(label)
                    self.projection_matrices[label] = Matrix.sparse(BOOL, self.size, self.size)
                self.projection_matrices[label][v_from, v_to] = True

            self.start_vertices = self.vertices
            self.final_vertices = self.vertices

    def read_regex(self, path):
        with open(path, 'r') as regex_file:
            regex = regex_file.readline().rstrip()
        dfa = Regex(regex).to_epsilon_nfa().to_deterministic().minimize()
        self.size = len(dfa.states)
        state_number = 0
        state_number_dict = dict()
        for state in dfa.states:
            state_number_dict[state] = state_number
            self.vertices.add(state_number)
            state_number += 1

        for v_from, label, v_to in dfa._transition_function.get_edges():
            if label not in self.labels:
                self.projection_matrices[label] = Matrix.sparse(BOOL, self.size, self.size)
                self.labels.add(label)
            self.projection_matrices[label][state_number_dict[v_from], state_number_dict[v_to]] = True

        for state in dfa.start_states:
            self.start_vertices.add(state_number_dict[state])

        for state in dfa.final_states:
            self.final_vertices.add(state_number_dict[state])

    # def add_start_states(self, path):
    #     if path is not None:
    #         with open(path, 'r') as start_states_file:
    #             self.start_vertices = set([int(state) for state in start_states_file.readline().split(" ")])
    #
    # def add_final_states(self, path):
    #     if path is not None:
    #         with open(path, 'r') as final_states_file:
    #             self.final_vertices = set([int(state) for state in final_states_file.readline().split(" ")])

    def intersect(self, graph):
        intersection = Graph()
        intersection.size = self.size * graph.size

        for label in self.labels:
            if label in graph.labels:
                intersection.labels.add(label)
                intersection.projection_matrices[label] = self.projection_matrices[label].kronecker(
                    graph.projection_matrices[label])

        for st1 in self.vertices:
            for st2 in graph.vertices:
                intersection_state = st1 * graph.size + st2
                intersection.vertices.add(intersection_state)
                if st1 in self.start_vertices and st2 in graph.start_vertices:
                    intersection.start_vertices.add(intersection_state)
                if st1 in self.final_vertices and st2 in graph.final_vertices:
                    intersection.final_vertices.add(intersection_state)

        return intersection

    def transitive_closure(self):
        closure = Matrix.sparse(BOOL, self.size, self.size)
        for label in self.labels:
            closure |= self.projection_matrices[label]

        prev_nvals = -1
        while prev_nvals != closure.nvals:
            prev_nvals = closure.nvals
            closure += closure @ closure

        return closure

    def reachable_with_start_states(self, start):
        result = self.transitive_closure()

        for state in range(self.size):
            if state not in start:
                result.assign_row(state, Vector.sparse(BOOL, self.size))

        return result

    def reachable_with_start_and_final_states(self, start, final):
        result = self.transitive_closure()

        for state in range(self.size):
            if state not in start:
                result.assign_row(state, Vector.sparse(BOOL, self.size))
            if state not in final:
                result.assign_col(state, Vector.sparse(BOOL, self.size))

        return result
