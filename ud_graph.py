# Course: CS261 W21
# Author: Elizabeth Ponce
# Assignment: Undirected Graphs
# Description: Assignment 6

import heapq 
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        This method adds a new vertex to the graph. Vertex names can be any string. 
        If vertex with the same name is already present in the graph, the method
        does nothing (no exception needs to be raised).
        """
        self.adj_list[v]= []

    def key_exists(self, key) -> bool:
        return key in self.adj_list.keys()  
    
    def add_edge(self, u: str, v: str) -> None:
        """
        This method adds a new edge to the graph, connecting two vertices with provided names. 
        
        If either (or both) vertex names do not exist in the graph, this method will first
        create them and then created an edge between them. 
        
        If an edge already exists in the 
        graph, or if u and v refer to the same vertex, the method does nothing (no exception
        needs to be raised).
        """

        if u == v:
            return 

        if not self.key_exists(u):
            self.add_vertex(u)

        if not self.key_exists(v):
            self.add_vertex(v)

        exists = False
        for i in self.adj_list[u]:
            if i == v:
                exists = True
        
        if exists == False:
            self.adj_list[u].append(v)
        
        exists = False
        for i in self.adj_list[v]:
            if i == u:
                exists = True

        if exists == False:
            self.adj_list[v].append(u)
        
    

    def remove_edge(self, v: str, u: str) -> None:
        """
        This method removes an edge between two vertices with provided names. 
        
        If either (or both) vertex names do not exist in the graph, 
        or if there is no edge between them,
        the method does nothing (no exception needs to be reaised).
        """
       
        if not self.key_exists(u):
            return

        if not self.key_exists(v):
            return

        exists = False
        for i in self.adj_list[u]:
            if i == v:
                exists = True

        if exists:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        This method removes a vertex with a given name and all edges incident to it from the graph.
        
        If the given vertex does not exist, the method does nothing (no exception to be raised).
        """
        if self.key_exists(v):
            for i in self.adj_list[v]:
                self.adj_list[i].remove(v)
            
            self.adj_list.pop(v)
        

    def get_vertices(self) -> []:
        """
        This method returns a list of vertices of the graph. 
        Order of the vertices in the list does not matter.
        """
        return list(self.adj_list.keys())

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph. Each edge is returned as a tuple 
        of two incident vertex names. Order of the edges in the list or order of the vertices
        incident to each edge does not matter.
        """
        edge_list = [] #list(self.adj_list.items())
        for v in self.adj_list:
            for av in self.adj_list[v]:
                tupe = (v, av)
                tupe_flip = (av, v)
                if tupe_flip not in edge_list:
                    edge_list.append(tupe)
                
        return edge_list

       


    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex names and returns True if the sequence of vertices represnts
        a valid path in the graph (so one can travel from the vertex in the list to the last vertex
        in the list, at each step traversing over an edge in the graph). Empty path is not
        considered valid.
        """

        if len(path) == 0:
            return True

        if len(path) == 1:
            return self.key_exists(path[0])

        cur = path[0]
        for v in path[1:]:
            if v in self.adj_list[cur]:
                cur = v
            else:
                return False

        return True

    def _dfs_helper(self, u, discovered, v_end=None) -> []:
        g = self.adj_list
        for v in sorted(g[u]):
        
            if v not in discovered:
                if v_end in discovered:
                    break
                discovered.append(v)
                self._dfs_helper(v, discovered, v_end)
        return discovered
        

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth-first search (DFS) in the graph and returns a list of vertices 
        visited during the search, in the order they were visited. It takes one required
        parameter, name of the vvertex from which the search will start, and one optional 
        parameter -- name of the 'end' vertex that will stop the search once the vertex is reached.

        If the starting vertex is not in the graph, the method should return an empty list 
        (no exception needs to be raised). 

        If the name of the 'end' vertex is provided but is not in the graph, the search should 
        be done as if there was no end vertex.

        When several options are avaialble for picking the next vertex to continue the search, your
        implementation should pick the vertices in ascending lexicographical order (so, for example,
        vertex 'APPLE' is explored before vertex 'BANANA').
        """
        discovered = [v_start]

        if v_start not in self.adj_list:
            return []

        return self._dfs_helper(v_start, discovered, v_end)


    def _bfs_helper(self, u, discovered, v_end=None) -> []:
        g = self.adj_list
        level = [u]
        
        while len(level) > 0:
            next_level = []
            for u in level:
                for v in sorted(g[u]):
                    if v not in discovered:
                        if v_end in discovered:
                            break
                        discovered.append(v)
                        next_level.append(v)
                level = next_level
        
        return discovered

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method works the same as the DFS above, except it implements a breadth-first search.
        """
        g = self.adj_list
        level = [v_start]

        if v_start not in g:
            return []
        
        return self._bfs_helper(v_start, level, v_end)
    
    #create a helper function that returns a list of vertices that are not in input list

    def missing_vertices(self, vert_list, fert_list) -> []:
        return list(set(vert_list).difference(fert_list))


    def count_connected_components(self) -> int:
        """
        This method returns the number of connected components in the graph.
        """
        to_find = self.get_vertices()
        # length = len(to_find)
        components_list = []
        found = []

        start_v = to_find[0]
        some_comp = self.dfs(start_v)
        found.extend(some_comp)
        components_list.append(some_comp)
        missing = self.missing_vertices(to_find, found)

        while len(missing) > 0:
            v_start = missing[0]
            some_comp = self.dfs(v_start)
            found.extend(some_comp)
            components_list.append(some_comp)
            missing = self.missing_vertices(to_find, found)
        
        return len(components_list)

    def has_cycle(self) -> bool:
        """
        This method returns True if there is at least one cycle in the graph. If the graph is acyclic,
        the method returns False.
        """
        num_verts = len(self.get_vertices())
        num_components = self.count_connected_components()
        num_edges = len(self.get_edges())

        test_cycle = num_verts - num_components
        if test_cycle == num_edges:
            return False
        else:
            return True
   
    
if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)

    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)

    # g.add_vertex('A')
    # print(g)

    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)


    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)


    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)}  BFS:{g.bfs(case)}') 
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}') 


    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
