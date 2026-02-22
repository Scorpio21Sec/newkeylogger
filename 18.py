#water jug problem for Ai Lab viva 
from collections import deque


def water_jug_problem(m,n,d):
    """
    Solve the Water Jug problem the traget given by ma'am is to reached 2 lit by using 7,3 lit jug
    here m is maximum capacity of 1st jug 
    n is capacity of 2nd jug
    and the last d is target amount of water
   
    
    """
    if d > max(m,n):
        return None
    
    visited = set()
    quque = deque()
    quque.append((0,0, [(0,0)]))
    visited.add((0,0))

    while quque:
        jug1, jug2, path = quque.popleft()
        if jug1 == d or jug2 == d:
            return path
        
        states = [
            (m,jug2),
            (jug1,n),
            (0,jug2),
            (jug1,0),
            ]
        pour_to_jug2 = min(jug1, n- jug2)
        states.append((jug1 - pour_to_jug2, jug2 + pour_to_jug2))
         
        
        pour_to_jug1 = min(jug2, m - jug1)
        states.append((jug1 + pour_to_jug1, jug2 - pour_to_jug1))
       
        for state in states:
            if state not in visited:
                visited.add(state)
                quque.append((state[0], state[1], path + [state]))
               
    return None

m,n,d = 7,3,2

solution_path= water_jug_problem(m,n,d)
if solution_path:
    print("Solution found")
    for state in solution_path:
        print(state)
else:
    print("No Solution Found ")
    





    
