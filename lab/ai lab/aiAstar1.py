import heapq

# Goal state of the puzzle
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.g = 0 if parent is None else parent.g + 1  # Cost to reach this node
        self.h = self.manhattan_distance()  # Heuristic cost to goal
        self.f = self.g + self.h # Total estimated cost

    def __lt__(self, other):
        return self.f < other.f

    def manhattan_distance(self):
        dist = 0
        for i, val in enumerate(self.state):
            if val == 0: continue
            goal_pos = GOAL.index(val)
            dist += abs(i % 3 - goal_pos % 3) + abs(i // 3 - goal_pos // 3)
        return dist

def get_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    r, c = zero_idx // 3, zero_idx % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            new_state_list = list(state)
            new_state_list[zero_idx], new_state_list[new_idx] = new_state_list[new_idx], new_state_list[zero_idx]
            neighbors.append(tuple(new_state_list))
    return neighbors

def a_star_search(start_state):
    # Check for solvability (inversions)
    inversions = 0
    flat_list = [i for i in start_state if i != 0]
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    if inversions % 2 != 0:
        return "Unsolvable puzzle"

    open_list = [Node(start_state)]
    closed_list = {start_state}

    while open_list:
        current_node = heapq.heappop(open_list)
        if current_node.state == GOAL:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1] # Return reversed path

        for neighbor_state in get_neighbors(current_node.state):
            if neighbor_state not in closed_list:
                closed_list.add(neighbor_state)
                heapq.heappush(open_list, Node(neighbor_state, current_node))
    return None

# --- Example Usage ---
start = (1, 2, 3, 4, 0, 5, 7, 8, 6)
solution = a_star_search(start)

if isinstance(solution, str):
    print(solution)
else:
    print(f"Solution found in {len(solution)-1} steps:")
    for i, state in enumerate(solution):
        print(f"\nStep {i}:")
        for j in range(0, 9, 3):
            print(state[j:j+3])