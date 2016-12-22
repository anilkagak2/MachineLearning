def displayPathtoPrincess(n,grid):
    #print all the moves here
    princess_loc = None
    my_loc = None

    for x in range(n):
        line = grid[x]
        for y in range(len(line)):
            if line[y] == 'm': my_loc = (x,y)
            elif line[y] == 'p': princess_loc = (x,y)

    #print(my_loc)
    #print(princess_loc)
    
    dy = princess_loc[0] - my_loc[0]
    dx = princess_loc[1] - my_loc[1]
    #print(dx)
    #print(dy)
    
    moves = []
    if dx > 0: moves.extend([ "RIGHT" ] * abs(dx))
    else: moves.extend([ "LEFT" ] * abs(dx))
    
    if dy > 0: moves.extend([ "DOWN" ] * abs(dy))
    else: moves.extend([ "UP" ] * abs(dy))
    print("\n".join(moves))

m = input()

grid = []
for i in xrange(0, m):
    grid.append(raw_input().strip())

displayPathtoPrincess(m,grid)