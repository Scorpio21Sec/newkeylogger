from collections import deque


def water_jug_bfs_with_path(m, n, d):
    """
    Solves the Water Jug Problem using Breadth-First Search (BFS).
    :param m: Capacity of the first jug.
    :param n: Capacity of the second jug.
    :param d: Target amount of water.
    :return: The shortest path of states (tuples) to reach the solution, or None.
    """
    # Simple check: the target must not exceed max capacity
    if d > max(m, n):
        return None


    visited = set()
    queue = deque()
    # Queue element: (jug1, jug2, path)
    queue.append((0, 0, [(0, 0)]))
    visited.add((0, 0))
   
    while queue:
        jug1, jug2, path = queue.popleft()
       
        # Check if the goal is reached
        if jug1 == d or jug2 == d:
            return path
           
        # --- Generate all possible next states (moves) ---
        states = [
            (m, jug2),       # Fill jug1
            (jug1, n),       # Fill jug2
            (0, jug2),       # Empty jug1
            (jug1, 0),       # Empty jug2
        ]
       
        # Pour jug1 -> jug2
        pour_to_jug2 = min(jug1, n - jug2)
        states.append((jug1 - pour_to_jug2, jug2 + pour_to_jug2))
       
        # Pour jug2 -> jug1
        pour_to_jug1 = min(jug2, m - jug1)
        states.append((jug1 + pour_to_jug1, jug2 - pour_to_jug1))
       
        for state in states:
            if state not in visited:
                visited.add(state)
                queue.append((state[0], state[1], path + [state]))
               
    return None


# Example usage: 7 liter jug, 3 liter jug, target 2 liters
m, n, d = 7, 3, 2
solution_path = water_jug_bfs_with_path(m, n, d)


if solution_path:
    print("States to reach the solution:")
    for state in solution_path:
        print(state)
else:
    print("No solution found.")
