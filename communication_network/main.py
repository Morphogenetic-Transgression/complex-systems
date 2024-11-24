import numpy as np
from graphviz import Digraph, Graph


COLORS = ['red',
          'green',
          'blue',
          'yellow',
          'purple',
          'silver',
          'orange',
          'pink'] # '0.051 0.718 0.627'

def rand_matrix(dimension: int, properties_num: int, agents_num: int) -> np.ndarray:
    return np.random.randint(dimension, size=(properties_num, agents_num))

def matrix_to_graph(matrix: np.ndarray,
                    name: str,
                    filename: str,
                    label: str) -> Graph:
    gra = Graph(name,
                filename=filename,
                # node_attr={'color': 'lightblue2',
                #            'style': 'filled'}
                ) # strict=True
    gra.attr(size='10,10')
    gra.attr(ratio='1,1')
    gra.attr(label=fr'\n{label}')
    gra.attr(fontsize='20')
    triplets = set()
    (properties_num, agents_num) = matrix.shape
    for agent_l in range(agents_num):
        for agent_r in range(agents_num):
            if agent_l != agent_r:
                for property in range(properties_num):
                    if matrix[property][agent_l] == matrix[property][agent_r]:
                        if matrix[property][agent_l] == 1: # property exists
                            if str(agent_l)+str(property)+str(agent_r) not in triplets:
                                gra.edge(str(agent_l), str(agent_r), color=COLORS[property])
                                triplets.add(str(agent_r)+str(property)+str(agent_l))
    return gra


if __name__ == '__main__':
    matrix = rand_matrix(dimension=2, properties_num=6, agents_num=10)
    print(matrix)
    print()
    # print((matrix[2][1], matrix[2][7]))
    graph = matrix_to_graph(matrix, 'cluster', "graph.gv", "Clusters")
    graph_path = graph.render(directory="graph_storage")
    print(graph_path)

