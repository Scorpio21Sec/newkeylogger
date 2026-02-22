class AOStar:
    def __init__(self, graph, heuristics, start_node):
        self.graph = graph
        self.heuristics = heuristics
        self.start_node = start_node
        self.parent = {}  # Stores the parent of a node in the optimal path
        self.status = {}  # Stores the status of the node (solved/unsolved)
        self.solution_graph = {} # Stores the final solution structure

    def applyAOStar(self):
        """
        Starts the AO* algorithm from the start node.
        """
        print("Starting AO* Search...")
        self.computeMinimumCostChildNodes(self.start_node)
        print("\nAO* Search Completed.")
        print("\nUpdated Heuristics (Costs):", self.heuristics)
        print("Optimal Solution Graph:", self.solution_graph)

    def computeMinimumCostChildNodes(self, v):
        """
        Recursively computes the minimum cost for node v.
        Updates the heuristic value of v based on its children.
        """
        # Check if current node is a leaf node (no neighbors defined in graph)
        if v not in self.graph:
            return self.heuristics.get(v, 0)

        minimumCost = float('inf')
        # Map each branch (tuple of child names) to (cost, [child_names])
        cost_to_child_branches = {}

        # Iterate over all possible branches (OR conditions)
        for childNodeList in self.graph[v]:
            cost = 0
            child_names = []

            # Iterate over individual nodes in a specific branch (AND conditions)
            for child, weight in childNodeList:
                # Recursive call to compute/update child's cost before using it
                child_cost = self.computeMinimumCostChildNodes(child)

                # Use the updated heuristic for the child if available, otherwise fallback
                cost += self.heuristics.get(child, child_cost) + weight
                child_names.append(child)

            # Store the computed cost and child name list for this specific branch
            # use tuple(child_names) as the key (always hashable) instead of tuple(childNodeList)
            cost_to_child_branches[tuple(child_names)] = (cost, child_names)

        # Find the minimum cost branch (The OR logic)
        best_child_names = []
        for key, (val, names) in cost_to_child_branches.items():
            if val < minimumCost:
                minimumCost = val
                best_child_names = names  # The best branch path (list of child node names)

        # Update the heuristic value of the current node to the new minimum cost
        self.heuristics[v] = minimumCost

        # Keep track of the solution path
        self.solution_graph[v] = best_child_names

        return minimumCost

def main():
    # ---------------------------------------------------------
    # GRAPH REPRESENTATION
    # Format: 'Node': [[('Child', Weight), ('Child', Weight)], ...]
    # Inner lists represent AND conditions (all must be solved).
    # Outer list represents OR conditions (choose one).
    # ---------------------------------------------------------
    
    # Example: A needs (B AND C) OR (D). 
    graph = {
        'A': [[('B', 1), ('C', 1)], [('D', 1)]],
        'B': [[('G', 1)], [('H', 1)]],
        'C': [[('J', 1)]],
        'D': [[('E', 1), ('F', 1)]],
        'G': [[('I', 1)]]
        # Nodes H, J, E, F, I are leaf nodes (no entry here)
    }

    # Initial Heuristic Values (Estimates)
    h = {
        'A': 1,
        'B': 6,
        'C': 2,
        'D': 12,
        'E': 2,
        'F': 1,
        'G': 5,
        'H': 7,
        'I': 1,
        'J': 1
    }

    print("Initial Graph Structure:", graph)
    print("Initial Heuristic Values:", h)
    print("-" * 50)

    # Run the Algorithm
    ao_star = AOStar(graph, h, 'A')
    ao_star.applyAOStar()

if __name__ == "__main__":
    main()