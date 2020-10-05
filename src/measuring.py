from src.graph import Graph
import time


def measure():
    graphs = ['LUBM300', 'LUBM500', 'LUBM1M', 'LUBM1.5M', 'LUBM1.9M']
    regs = ['q1_0', 'q2_0', 'q3_0', 'q4_2_0', 'q5_0', 'q6_0', 'q7_0', 'q8_0', 'q9_2_0',
            'q10_2_0', 'q11_2_0', 'q_12_0', 'q_13_0', 'q_14_0', 'q_15_0', 'q_16_0']

    for graph in graphs:

        graph1 = Graph()
        graph1.read_graph(f"{graph}/{graph}.txt")

        for reg in regs:

            graph2 = Graph()
            graph2.read_regex(f"{graph}/regexes/{reg}")

            intersection_time = 0
            intersection = graph1.intersect(graph2)
            for i in range(5):
                start = time.time()
                graph1.intersect(graph2)
                end = time.time()
                intersection_time += end - start

            closure_square_time = 0
            for i in range(5):
                start = time.time()
                intersection.transitive_closure_square()
                end = time.time()
                closure_square_time += end - start

            closure_mul_time = 0
            for i in range(5):
                start = time.time()
                intersection.transitive_closure_mul()
                end = time.time()
                closure_mul_time += end - start

            with open("data/results.txt", "a") as out:
                out.write(f"{graph} {reg} results:\nintersection_time = {intersection_time/5}\n"
                          f"closure_square_time = {closure_square_time/5}\nclosure_mul_time = {closure_mul_time/5}\n")

            print("query ended")
