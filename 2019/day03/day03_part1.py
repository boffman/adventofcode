import math

def apply_move(maze, x, y):
    key = "{},{}".format(x,y)
    maze.add(key)

def calc_distance(key):
    x, y = [int(v) for v in key.split(",")]
    return abs(x) + abs(y)

def find_smallest_distance(maze):
    min_distance = None

    for key in maze:
        distance = calc_distance(key)
        print("Intersection at {} - distance = {}".format(key, distance))
        if not min_distance or distance < min_distance:
            min_distance = distance

    if min_distance is None:
        raise Exception("Failed to find distances in maze")

    return min_distance


def apply_moves(moves, maze):    
    x = 0
    y = 0

    for move in moves:
        direction, distance = move[0], int(move[1:])
        if direction == "U":
            for y in range(y+1, y+distance+1):
                apply_move(maze, x, y)
        elif direction == "D":
            for y in range(y-1, y-distance-1, -1):
                apply_move(maze, x, y)
        elif direction == "R":
            for x in range(x+1, x+distance+1):
                apply_move(maze, x, y)
        elif direction == "L":
            for x in range(x-1, x-distance-1, -1):
                apply_move(maze, x, y)
        else:
            raise Exception("Unknown direction: {}".format(direction,))

maze1 = set()
maze2 = set()
with open("input") as infile:
    moves1 = infile.readline().strip().split(",")
    apply_moves(moves1, maze1)

    moves2 = infile.readline().strip().split(",")
    apply_moves(moves2, maze2)

merge_maze = maze1 & maze2

distance = find_smallest_distance(merge_maze)
print(distance)