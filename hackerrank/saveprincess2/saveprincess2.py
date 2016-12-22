moves = []

def nextMove(n,r,c,grid):
    global moves
    if len(moves) == 0:
        rp,cp = 0,0
        for row in range(n):
            for col in range(n):
                if grid[row][col] == 'p':
                    rp,cp = row,col
                    break

        dy = rp - r
        dx = cp - c

        if dx > 0: moves.extend([ "RIGHT" ] * abs(dx))
        else: moves.extend([ "LEFT" ] * abs(dx))
    
        if dy > 0: moves.extend([ "DOWN" ] * abs(dy))
        else: moves.extend([ "UP" ] * abs(dy))
        #print(moves)
    
    move = moves[0]
    moves = moves[1:]
    return move

n = input()
r,c = [int(i) for i in raw_input().strip().split()]
grid = []
for i in xrange(0, n):
    grid.append(raw_input())

print nextMove(n,r,c,grid)
print nextMove(n,r,c,grid)
print nextMove(n,r,c,grid)
