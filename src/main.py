from argparse import ArgumentParser
from graph import Graph


def read_vertices(path):
    with open(path, 'r') as f:
        return set([int(i) for i in f.readline().split(' ')])


def main():
    parser = ArgumentParser()

    parser.add_argument(
        '--graph',
        required=True,
        type=str
    )

    parser.add_argument(
        '--regex',
        required=True,
        type=str
    )
    # parser.add_argument(
    #     '--start_states',
    #     required=False,
    # )
    # parser.add_argument(
    #     '--final_states',
    #     required=False
    # )

    args = parser.parse_args()

    graph = Graph()
    graph.read_graph(args.graph)
    # graph.add_start_states(args.start_states)
    # graph.add_final_states(args.final_states)
    regex = Graph()
    regex.read_regex(args.regex)

    intersection = graph.intersect(regex)
    closure = intersection.transitive_closure()
    intersection.reachable_with_start_states([0])
    print('Edges for each label:')

    for label in intersection.labels:
        print(str(intersection.projection_matrices[label].nvals) + " of label " + str(label))

    print("-------------")
    print(graph.vertices)
    print(graph.labels)
    print(graph.start_vertices)
    print(graph.final_vertices)
    print(graph.projection_matrices)

    # closure = intersection.transitive_closure()
    #
    # print('Reachable vertices:')
    #
    # reachable = BMGraph.get_reachable_vertices(closure)
    # for (v_from, v_to) in reachable:
    #     if v_from in intersection.start_states and v_to in intersection.final_states:
    #         print('{} -> {}'.format(v_from // regex.states_amount,
    #                                 v_to // regex.states_amount))


if __name__ == "__main__":
    main()
