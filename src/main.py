from argparse import ArgumentParser
from src.graph import Graph


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

    args = parser.parse_args()

    graph = Graph()
    graph.read_graph(args.graph)
    regex = Graph()
    regex.read_regex(args.regex)

    intersection = graph.intersect(regex)
    closure = intersection.transitive_closure_square()

    print('Edges for each label:')

    for label in intersection.labels:
        print(f"{intersection.projection_matrices[label].nvals} of label {label}")


if __name__ == "__main__":
    main()
