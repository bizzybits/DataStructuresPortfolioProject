# Course: CS261 - Data Structures
# Author: Elizabeth Ponce
# Assignment: Directed Graphs
# Description: Assignment 6

import heapq 
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        This method adds a new vertex to the graph. Vertex does not need to be provided,
        instead vertex will be assigned a reference index (integer). 
        
        First vertex created in the graph will be assigned index 0.
        The subsequent vertices will have indexes 1, 2, 3, etc.
        
        This method returns a single integer - the number of vertices after the addition.
        """
        for i in range(self.v_count):
            self.adj_matrix[i].append(0)
        
        new_list = [0] * (self.v_count + 1)
        self.adj_matrix.append(new_list)
        self.v_count += 1

        return self.v_count
    
    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        This method adds a new edge to the graph, connecting the two vertices with provided indices.
        
        If either (or both) vertex indicies do not exist in the graph, or 
        if the weight is not a positive integer, or 
        if src and dst refer to the same index, the method does nothing.

        If an edge already exists in the graph, the method will update its weight.
        """

        if src == dst:
            return 

        if src >= self.v_count:
            return 

        if dst >= self.v_count:
            return 

        if weight < 0:
            return
    
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method removes an edge between two vertices with provided indices.
        
        If either (or both) vertex indeices do not exist in the graph,
        OR there is no edge between them, the method does nothing (no exception needs to be raised.)
        """

        if (src < 0) or (dst < 0):
            return 

        if (src >= len(self.get_vertices())) or (dst >= len(self.get_vertices())):
            return

        if self.adj_matrix[src][dst] == 0:
            return 

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        This method returns a list of vertices of the graph.
        Order of the vertices does not matter.
        """

        return list(range(self.v_count))

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph. 
        Each edge is returned as a tuple of two incident vertex indices and weight. 

        First element in the tuple refers to the source vertex. 
        Second element in the tuple refers to the destination vertex. 
        Third element in the tuple is the weight of the edge.
        Order of the edges does not matter.
        """
        edge_list = []

        for r in range(self.v_count):
            for c in range(self.v_count):
                weight = self.adj_matrix[r][c]
                if self.adj_matrix[r][c] != 0:
                    tupe = (r, c, weight)
                    edge_list.append(tupe)

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex indices and returns True if the sequence of vertices
        represents a valid path in the graph (so one can travel from the fist vertex in the list 
        to the last vertex in the list, at each step traversing over an edge in the graph). 
        
        Empty path is considered valid. 
        """
        if len(path) == 0:
            return True

        if len(path) == 1:
            return True

        cur = path[0]
        for v in path[1:]:
            if v < 0:
                return False
            if self.adj_matrix[cur][v] != 0:
                cur = v
            else:
                return False
        return True
        
    def _dfs_helper(self, u, discovered,result, v_end=None) -> []:

        result.append(u)
        discovered[u] = True
     
        for i in range(len(self.adj_matrix[u])):
            if (self.adj_matrix[u][i] != 0 and (not discovered[i])): 
                self._dfs_helper(i, discovered, result) 
       
        return result



    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth-first search (DFS) in the graph and returns a list
        of vertices visited during the search, in the order they were visited. It takes one
        required parameter, index of the vertex from which the search will start, and one 
        optional parameter - index of the 'end' vertex that will stop the search once 
        that vertex is reached.

        If the starting vertex is not in the graph, the method should return an empty list
        (no exception needs to be raised). If the 'end' vertex is provided but is not in the 
        graph, the search should be done as if there was no end vertex.

        When several options are available for picking the next vertex to continue the search, 
        your implementation should pick the vertices by vertex in ascenting order (so, for 
        example, vertex 5 is explored before vertex 6).

        Inspiration from G4G:
        https://www.geeksforgeeks.org/implementation-of-dfs-using-adjacency-matrix/
        """
        discovered = [False] * self.v_count
        result = []

        if v_start not in self.get_vertices():
            return []

        return self._dfs_helper(v_start, discovered, result)

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method works the same as DFS above, except it implements a breadth-first search.
        """
        to_visit = deque()
        to_visit.append(v_start)

        visited = []

        while len(to_visit) > 0:
            v = to_visit.popleft()
            visited.append(v)
            for i in range(len(self.adj_matrix[v])):
                if self.adj_matrix[v][i] != 0:
                    if i not in visited and i not in to_visit:
                        to_visit.append(i)

        return visited

    def _has_cycle_helper(self, v, visited, stack):

        visited[v] = True
        stack[v] = True

        for sibling in range(len(self.get_vertices())): 
            if self.adj_matrix[v][sibling] != 0:
                if visited[sibling] == False: 
                    if self._has_cycle_helper(sibling, visited, stack) == True: 
                        return True
                elif stack[sibling] == True: 
                    return True

        stack[v] = False
        return False

    def has_cycle(self) -> bool:
        """
        This method returns True if there is at least once cycle in the graph.
        If the graph is acyclic, the method returns False.

        This method and the helper were inspired by G4G:
        https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
        """
        visited = [False] * self.v_count 
        stack = [False] * self.v_count 
        for node in range(len(self.get_vertices())): 
            if visited[node] == False: 
                if self._has_cycle_helper(node,visited,stack) == True: 
                    return True

        return False
        

    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length of the shortest
        path from a given vertex to all other vertices in the graph. 

        It returns a list with one value per each vertex in the graph, where value at index 0 
        is the length of the shortest path from vertex SRC to vertex 0, 
        value at index 1 is the length of the shortest path from vertex SRC to vertex 1, etc.

        If a certain vertex is not reachable from SRC, 
        return value should be INFINITY (in Python, use float('int)).
        """
        distances = {} #creating a hashmap and populating with infinity as distance to each vertex from src
        for i in range(len(self.adj_matrix)):
            distances[i] = float('inf')

        distances[src] = 0 #distance from the source to itself is 0
        priority_queue = [(0, src)] #priority queue to evaluate distance

        while len(priority_queue) > 0: #while there are items in the queue
            current_distance, current_vertex = heapq.heappop(priority_queue) 
            #variables are created current_distance = first half of tuple 
            #variables are created current_vertex = second half of tuple
            if current_distance > distances[current_vertex]:
                continue
            #if the current distance to the vertex is greater than the distance held in dictionary
            for sibling in range(len(self.adj_matrix[current_vertex])): 
                #check all next vertices from the current vertex
                weight = self.adj_matrix[current_vertex][sibling]
                #assigning the weight variable from the confluence of current vertex and it's sibling
                if weight > 0:
                    distance = current_distance + weight
                    #if weight is greater than 0, update distance to sum of current_distance 
                    #and the weight of the new edge (distance = total cost to get from src to sibling)
                    if distance < distances[sibling]:
                        #if the new distance is less than the distance of the sibling held in the dictionary
                        distances[sibling] = distance
                        #update lesser distance 
                        heapq.heappush(priority_queue, (distance, sibling))
                        #add the tuple to the priority queue
                        
        return list(distances.values())




if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)

    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)


    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)

    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')

    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
