import heapq

# Goal state
G = (1,2,3,4,5,6,7,8,0)

def manhattan(s):
    return sum(0 if v==0 else abs((i:=s.index(v))//3 - ((v-1)//3)) + abs(i%3 - (v-1)%3) for v in s)

def neighbors(s):
    z=s.index(0); r,c=divmod(z,3)
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0<=nr<3 and 0<=nc<3:
            ns = list(s); ni = nr*3+nc
            ns[z], ns[ni] = ns[ni], ns[z]
            yield tuple(ns)

def solvable(s):
    inv=sum(1 for i in range(9) for j in range(i+1,9) if s[i] and s[j] and s[i]>s[j])
    return inv%2==0

def a_star(start):
    if not solvable(start): return 'Unsolvable puzzle'
    pq=[]; seen={start:0}
    heapq.heappush(pq,(manhattan(start),0,start,None))  # (f, g, state, parent)
    parents={start:None}
    while pq:
        f,g,s,par = heapq.heappop(pq)
        if s==G:
            path=[]
            while s: path.append(s); s=parents[s]
            return path[::-1]
        for ns in neighbors(s):
            ng=g+1
            if ng<seen.get(ns,1e9):
                seen[ns]=ng; parents[ns]=s
                heapq.heappush(pq,(ng+manhattan(ns),ng,ns,s))
    return None

def print_solution(p):
    if isinstance(p,str):
        print(p); return
    print('Solution found! Steps:',len(p)-1)
    for i,s in enumerate(p):
        print('\nStep',i)
        for r in range(0,9,3): print(s[r:r+3])

if __name__=='__main__':
    start=(1,2,3,4,0,5,7,8,6)
    print_solution(a_star(start))
    print_solution(a_star((8,6,7,2,5,4,3,0,1)))