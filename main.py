import sys
import logging
from logging import debug as D
import pretty_errors

MAX_INT = sys.maxsize

def main():
    # vertices = input_vertices()
    # edges = input_edges(vertices)

    # SEE: https://www.startpage.com/av/proxy-image?piurl=https%3A%2F%2Fencrypted-tbn0.gstatic.com%2Fimages%3Fq%3Dtbn%3AANd9GcQL29F6ecFDdMxNje3xl6kiminWfcoAlEKrum4_Iv1A4_qqrXs%26s&sp=1655735612Te0cff05481043c27f94400a7547718e74afb92ae81c3886d227543a1bcdc8ad6
    # vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    # edges = [
    #     Edge('CE', 3),
    #     Edge('AB', 10),
    #     Edge('AC', 12),
    #     Edge('BC', 9),
    #     Edge('BD', 8),
    #     Edge('EF', 3),
    #     Edge('CF', 1),
    #     Edge('DH', 5),
    #     Edge('FH', 6),
    #     Edge('DG', 8),
    #     Edge('GH', 9),
    #     Edge('GI', 2),
    #     Edge('ED', 7),
    #     Edge('IH', 11)
    # ]
    # SEE: https://www.startpage.com/av/proxy-image?piurl=https%3A%2F%2Fencrypted-tbn0.gstatic.com%2Fimages%3Fq%3Dtbn%3AANd9GcRZKvlnjJZ63-gdl9T2Zi6xWTiZF0ZaMUKy3QwhF0robrrzCYR9%26s&sp=1655735612T26396ecb90dccded2c26db96844e3371ad3f47e5aad83a6441c0aa5d4e2279ea
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        Edge('AB', 15),
        Edge('AC', 9),
        Edge('CD', 23),
        Edge('DB', 6),
        Edge('AE', 1),
        Edge('BE', 18),
        Edge('CE', 4),
        Edge('DE', 11)
    ]
    
    # mst_prims = MST(vertices, edges).generate_using_prims_algorithm()
    mst_kruskals = MST(vertices, edges).generate_using_kruskals_algorithm()
    
    # print("\n\nPrim's MST:", end=' ')
    # print_edges(mst_prims)
    # print()
    print("\n\nKruskal's MST:", end=' ')
    print_edges(mst_kruskals)
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
    available_edges = eliminate_duplicates_from_list(available_edges)
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
        self.name = string.upper()
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
        length = self.length
        is_positive_int = type(length) is int and length>0 
        if is_positive_int or length.isnumeric():
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
        if (vertex_1 in vertices) and (vertex_2 in vertices):
            return True
        else:
            return False


# NOTE: MST stands for Minimum Spanning Tree.
class MST():
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.mst = []


    def generate_using_prims_algorithm(self):
        available_vertices = self.vertices[0]
        all_vertices_added = False
        while not all_vertices_added:
            available_edges = get_edges_from_vertices(self.edges, available_vertices)
            
            min_edge = self.__find_min_edge(available_vertices, available_edges)

            # NOTE: Handles a special case when there is only one entered edge.
            if min_edge is None:
                break

            self.mst.append(min_edge)
            available_vertices = get_vertices_from_edges(self.mst)
            all_vertices_added = len(available_vertices)==len(self.vertices)

        return self.mst


    def __find_min_edge(self, vertices, edges):
        min_edge = None
        min_len = MAX_INT

        for cur_edge in edges:
            forms_a_loop = cur_edge.exists(vertices)
            if cur_edge in self.mst or forms_a_loop:
                continue

            cur_len = cur_edge.get_length()
            if cur_len < min_len:
                min_len = cur_len
                min_edge = cur_edge

        return min_edge


    def generate_using_kruskals_algorithm(self):
        available_edges = self.edges
        self.mst.append(self.__find_min_edge(self.vertices[0-1], self.edges))
        list_of_msts = []
        while len(available_edges) > 1:
            min_edge = None
            min_len = MAX_INT

            for cur_edge in available_edges:

                if cur_edge in self.mst:
                    continue

                cur_len = cur_edge.get_length()
                if cur_len < min_len:
                    min_len = cur_len
                    min_edge = cur_edge

            mst_vertices = [ mst_edge.get_vertices() for mst_edge in self.mst ]

            #1: Min edge is already a part of MST.
            if min_edge is None or min_edge.exists(mst_vertices):
                continue

            min_edge_vertex_1 = min_edge.get_vertices()[0]
            min_edge_vertex_2 = min_edge.get_vertices()[1]

            for cur_mst in list_of_msts:
                if cur_mst is None:
                    continue

                cur_mst_vertices = [ cur_mst_edge.get_vertices() for cur_mst_edge in cur_mst ]

                for cur_mst_edge in cur_mst:
                    vertices_of_cur_mst_edge = cur_mst_edge.get_vertices()
                    has_first_vertex = min_edge_vertex_1 in vertices_of_cur_mst_edge 
                    has_second_vertex = min_edge_vertex_2 in vertices_of_cur_mst_edge
                    min_edge_is_part_of_cur_mst = (has_first_vertex) or (has_second_vertex)
                    already_exists_or_forms_a_loop = min_edge.exists(cur_mst_vertices)

                    #2: Min edge belongs to one of the MSTs in list_of_msts.
                    if min_edge_is_part_of_cur_mst and not already_exists_or_forms_a_loop:
                        cur_mst.append(min_edge)
                    else:
                        new_mst = [ min_edge ]
                        list_of_msts.append(new_mst)

                list_of_msts.append(cur_mst)

            self.mst.append(list_of_msts)
            available_edges.remove(min_edge)


        return self.mst


if __name__ == '__main__':
    pretty_errors.configure(
        lines_before         = 10,
        separator_character  = '',
        line_number_first    = True,
        display_locals       = True,
        display_trace_locals = True,
        filename_color       = pretty_errors.CYAN,
        code_color           = pretty_errors.WHITE,
        exception_arg_color  = pretty_errors.YELLOW,
        local_name_color     = pretty_errors.BLUE,
        function_color       = pretty_errors.BRIGHT_GREEN,
        line_number_color    = pretty_errors.BRIGHT_YELLOW,
        line_color           = pretty_errors.RED + '> ' + pretty_errors.default_config.local_value_color,
        infix = '────────────────────────────────────────────────────────────────────────────────'
    )

    logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] -----> [%(lineno)s]: %(msg)s')

    main()
