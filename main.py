import sys
import logging
from logging import debug as D

logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] -----> [%(lineno)s]: %(msg)s')

MAX_INT = sys.maxsize


def main():
    vertices = input_vertices()
    edges = input_edges(vertices)

    mst = MST(vertices, edges).generate_list_of_edges()
    
    print('\n\nMST:', end=' ')
    print_edges(mst)
    print()


def input_vertices():
    inp_vertices = input('Please input vertices (A-Z): ')
    vertices = get_list_of_vertices_from_string(inp_vertices)
    vertices = eliminate_duplicates_from_list(vertices)

    print('\nEntered vertices:', end=' ')
    print_vertices(vertices)
    return vertices


def get_list_of_vertices_from_string(string):
    vertices = []
    if type(string) is not str:
        raise TypeError(f'"{string}" is "{type(string)}", not a string.')

    for char in string:
        vertex = Vertex(char)
        if vertex.is_valid():
            vertices.append(vertex.get_name())
        else:
            print(f'WARNING: Invalid vertex "{char}". Skipping...')

    return vertices


def eliminate_duplicates_from_list(list_):
    return list(dict.fromkeys(list_))


def print_vertices(vertices):
    vertices.sort()
    for vertex in vertices:
        print(vertex, end=' ')
    print('\n')


def input_edges(vertices):
    edges = []
    while True:
        inp_edge = input('Enter an edge (AB-YZ): ')
        if inp_edge == 'q' or inp_edge == 'Q': 
            break

        edge = Edge(inp_edge, None)

        if not edge.name_is_valid():
            print(f'ERROR: invalid edge "{inp_edge}"')
            continue

        edge_name = edge.get_name()

        if not edge.exists(vertices):
            print(f'ERROR: "{edge_name}" does not exist.')
            continue

        if edge_is_duplicate(edge_name, edges):
            print(f'ERROR: edge {edge_name} already exists.')
            continue

        inp_length = input(f'Enter {edge_name} length: ')

        if not inp_length.isnumeric():
            print(f'ERROR: edge length must be an integer.')
            continue

        try:
            edge.set_length(inp_length)
        except ValueError as e:
            print(e)
            continue

        edges.append(edge)

    print('\nEntered edges:', end=' ')
    print_edges(edges)
    return edges


def edge_is_duplicate(edge_name, existing_edges):
    for existing_edge in existing_edges:
        existing_edge_name = existing_edge.get_name()
        if edge_name == existing_edge_name:
            return True

    return False


def print_edges(edges):
    for edge in edges:
        name = edge.get_name()
        length = edge.get_length()
        print(f'[{name}]={length}', end=' ')


def get_edges_from_vertices(edges, vertices):
    available_edges = []
    for vertex in vertices:
        for edge in edges:
            edge_vertices = edge.get_vertices()
            if vertex == edge_vertices[0] or vertex == edge_vertices[1]:
                available_edges.append(edge)
    return available_edges


def get_vertices_from_edges(edges):
    vertices = []
    for edge in edges:
        edge_vertices = edge.get_vertices()
        vertices.append(edge_vertices[0])
        vertices.append(edge_vertices[1])
    vertices = eliminate_duplicates_from_list(vertices)
    return vertices


class Vertex():
    def __init__(self, name):
        self.name = str(name)


    def get_name(self):
        if self.is_valid():
            return self.__capitilize()
        else:
            raise ValueError(f'Invalid vertex "{self.name}".')


    def is_valid(self):
        if self.name.isalpha():
            return True
        else:
            return False


    def __capitilize(self):
        return self.name.upper()


class Edge():
    def __init__(self, string, length):
        try:
            string = string.upper()
        except:
            pass
        self.name = string
        self.length = length


    def get_name(self):
        if self.name_is_valid():
            vertices = self.get_vertices()
            return vertices[0] + vertices[1]
        else:
            raise ValueError(f'Invalid edge name "{self.name}".')


    def get_length(self):
        if self.length_is_valid():
            return int(self.length)
        else:
            raise ValueError(f'Invalid edge length "{self.length}".')


    def get_vertices(self):
        if self.name_is_valid():
            vertices = [ self.name[0], self.name[1] ] 
            vertices.sort()
            return vertices
        else:
            raise ValueError(f'Invalid edge "{self.name}".')


    def set_length(self, length):
        self.length = length
        if not self.length_is_valid():
            raise ValueError(f'Invalid length "{length}".')


    def length_is_valid(self):
        if self.length.isnumeric():
            return True
        else:
            return False


    def name_is_valid(self):
        if len(self.name)==2 and self.name.isalpha():
            return True
        else:
            return False


    def exists(self, vertices):
        vertex_1 = self.get_vertices()[0]
        vertex_2 = self.get_vertices()[1]
        if (vertex_1 and vertex_2) in vertices:
            return True
        else:
            return False


# NOTE: MST stands for Minimum Spanning Tree.
class MST():
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


    def generate_list_of_edges(self):
        mst = []
        available_vertices = self.vertices[0]
        while len(available_vertices) != len(self.vertices):
            available_edges = get_edges_from_vertices(self.edges, available_vertices)

            min_edge_len = MAX_INT
            min_edge = None

            for edge in available_edges:
                if edge in mst:
                    continue
                length = edge.get_length()
                if length < min_edge_len:
                    min_edge_len = length
                    min_edge = edge

            mst.append(min_edge)
            available_vertices = get_vertices_from_edges(mst)
        return mst


if __name__ == '__main__':
    main()
