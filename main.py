import sys
import logging
from logging import debug as D

logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] -----> [%(lineno)s]: %(msg)s')

BIG_NUM = sys.maxsize

def main():
    inp_vertices = input('Please input vertices (A-Z): ')
    vertices = []
    for vertex in inp_vertices:
        if vertex.isalpha():
            vertices.append(vertex.upper())

    vertices = list(dict.fromkeys(vertices))
    D(vertices)

    edges = {}

    vertex1 = '' 
    vertex2 = '' 
    while True:
        edge = input('Enter the edge (AB-YZ): ')
        if edge == 'q' or edge == 'Q': 
            break
        if len(edge) > 2 or not edge.isalpha():
            print(f'ERROR: edge can only be two letters')
            continue

        edge = edge.upper()

        try:
            vertex1 = edge[0]
            vertex2 = edge[1]
        except:
            print(f'ERROR: incorrect edge "{edge}"')
            continue

        if not (vertex1 and vertex2) in inp_vertices:
            print(f'ERROR: "{edge}" does not exist.')
            continue

        edge_len = input(f'Enter {edge} length: ')
        if not edge_len.isnumeric():
            print(f'ERROR: edge length must be an integer.')
            continue

        edges[edge] = edge_len
        D(edges)

    min_edge_len = BIG_NUM
    available_edges = {}
    mst = {}
    # WIP
    for vertex in vertices:
        for edge, edge_len in edges.items():
            vertex1 = edge[0]
            vertex2 = edge[1]
            if vertex == vertex1 or vertex == vertex2:
                available_edges[edge] = edge_len

        min_edge_len = min(available_edges.values())

        # NOTE: Get key by value
        edge = list(available_edges.keys())[list(available_edges.values()).index(min_edge_len)]

        mst[edge] = min_edge_len

    D(mst)


if __name__ == '__main__':
    main()
