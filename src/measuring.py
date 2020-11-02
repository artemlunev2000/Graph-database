from src.graph import Graph
from src.grammar import Grammar
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

def measure_cfpq():
    Fgraphs = ['fullgraph_10', 'fullgraph_50', 'fullgraph_100', 'fullgraph_200', 'fullgraph_500']
    MAgraphs = ['bzip2.txt', 'gzip.txt', 'ls.txt', 'pr.txt', 'wc.txt']
    Sgraphs = ['G5k-0.001', 'G10k-0.001', 'G10k-0.01', 'G10k-0.1', 'G20k-0.001', 'G40k-0.001', 'G80k-0.001']
    WCgraphs = ['worstcase_4', 'worstcase_8', 'worstcase_16', 'worstcase_32', 'worstcase_64', 'worstcase_128']


    for graph in MAgraphs:

        graph1 = Graph()
        graph1.read_graph(f"MemoryAliases/graphs/{graph}")

        grammar = Grammar()
        gr = grammar.read_grammar("MemoryAliases/grammars/g1")

        hellings_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            hellings_res = Grammar.hellings_algo(gr, graph_copy)
            end = time.time()
            hellings_time += end - start

        cfpq_mul_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_mul_res = Grammar.cfpq_multiplication(gr, graph_copy)
            end = time.time()
            cfpq_mul_time += end - start

        cfpq_tensor_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_res = Grammar.cfpq_tensor(gr, graph_copy)
            end = time.time()
            cfpq_tensor_time += end - start

        gr_normal = gr.to_normal_form()
        cfpq_tensor_normal_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_normal_res = Grammar.cfpq_tensor(gr_normal, graph_copy)
            end = time.time()
            cfpq_tensor_normal_time += end - start

        with open("results_MA.txt", "a") as out:
            out.write(f"{graph} g1 results:\nhellings_time = {hellings_time/3}\n"
                      f"cfpq_mul_time = {cfpq_mul_time/3}\ncfpq_tensor_time = {cfpq_tensor_time/3}\n"
                      f"cfpq_tensor_normal_time = {cfpq_tensor_normal_time/3}\n")

        print(f"query for {graph} ended")


    for graph in WCgraphs:

        graph1 = Graph()
        graph1.read_graph(f"WorstCase/graphs/{graph}")

        grammar = Grammar()
        gr = grammar.read_grammar("WorstCase/grammars/g1")

        hellings_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            hellings_res = Grammar.hellings_algo(gr, graph_copy)
            end = time.time()
            hellings_time += end - start

        cfpq_mul_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_mul_res = Grammar.cfpq_multiplication(gr, graph_copy)
            end = time.time()
            cfpq_mul_time += end - start

        cfpq_tensor_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_res = Grammar.cfpq_tensor(gr, graph_copy)
            end = time.time()
            cfpq_tensor_time += end - start

        gr_normal = gr.to_normal_form()
        cfpq_tensor_normal_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_normal_res = Grammar.cfpq_tensor(gr_normal, graph_copy)
            end = time.time()
            cfpq_tensor_normal_time += end - start

        with open("results_WC.txt", "a") as out:
            out.write(f"{graph} g1 results:\nhellings_time = {hellings_time/3}\n"
                      f"cfpq_mul_time = {cfpq_mul_time/3}\ncfpq_tensor_time = {cfpq_tensor_time/3}\n"
                      f"cfpq_tensor_normal_time = {cfpq_tensor_normal_time/3}\n")

        print(f"query for {graph} ended")

    for graph in Sgraphs:

        graph1 = Graph()
        graph1.read_graph(f"SparseGraph/graphs/{graph}")

        grammar = Grammar()
        gr = grammar.read_grammar("SparseGraph/grammars/g1")

        hellings_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            hellings_res = Grammar.hellings_algo(gr, graph_copy)
            end = time.time()
            hellings_time += end - start

        cfpq_mul_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_mul_res = Grammar.cfpq_multiplication(gr, graph_copy)
            end = time.time()
            cfpq_mul_time += end - start

        cfpq_tensor_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_res = Grammar.cfpq_tensor(gr, graph_copy)
            end = time.time()
            cfpq_tensor_time += end - start

        gr_normal = gr.to_normal_form()
        cfpq_tensor_normal_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_normal_res = Grammar.cfpq_tensor(gr_normal, graph_copy)
            end = time.time()
            cfpq_tensor_normal_time += end - start

        with open("results_Sparse.txt", "a") as out:
            out.write(f"{graph} g1 results:\nhellings_time = {hellings_time/3}\n"
                      f"cfpq_mul_time = {cfpq_mul_time/3}\ncfpq_tensor_time = {cfpq_tensor_time/3}\n"
                      f"cfpq_tensor_normal_time = {cfpq_tensor_normal_time/3}\n")

        print(f"query for {graph} ended")

    for graph in Fgraphs:

        graph1 = Graph()
        graph1.read_graph(f"FullGraph/graphs/{graph}")

        grammar = Grammar()
        gr = grammar.read_grammar("FullGraph/grammars/g1")

        hellings_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            hellings_res = Grammar.hellings_algo(gr, graph_copy)
            end = time.time()
            hellings_time += end - start

        cfpq_mul_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_mul_res = Grammar.cfpq_multiplication(gr, graph_copy)
            end = time.time()
            cfpq_mul_time += end - start

        cfpq_tensor_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_res = Grammar.cfpq_tensor(gr, graph_copy)
            end = time.time()
            cfpq_tensor_time += end - start

        gr_normal = gr.to_normal_form()
        cfpq_tensor_normal_time = 0
        for i in range(3):
            graph_copy = graph1.copy()
            start = time.time()
            cfpq_tensor_normal_res = Grammar.cfpq_tensor(gr_normal, graph_copy)
            end = time.time()
            cfpq_tensor_normal_time += end - start

        with open("results_Full.txt", "a") as out:
            out.write(f"{graph} g4 results:\nhellings_time = {hellings_time/3}\n"
                      f"cfpq_mul_time = {cfpq_mul_time/3}\ncfpq_tensor_time = {cfpq_tensor_time/3}\n"
                      f"cfpq_tensor_normal_time = {cfpq_tensor_normal_time/3}\n")

        print(f"query for {graph} ended")
