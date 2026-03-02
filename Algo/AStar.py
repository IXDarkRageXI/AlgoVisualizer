import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze):
    rows, cols = maze.rows, maze.cols
    start, end = maze.start, maze.end
    grid = maze.grid

    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = {start: 0}
    parent = {}
    visited = set()
    order = []

    while open_set:
        _, current = heapq.heappop(open_set)
        order.append(current)

        if current == end:
            break

        visited.add(current)

        x, y = current
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            neighbor = (x + dx, y + dy)

            if (0 <= neighbor[0] < rows and
                0 <= neighbor[1] < cols and
                grid[neighbor[0]][neighbor[1]] == 0):

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))
                    parent[neighbor] = current

    path = []
    node = end
    while node in parent:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()

    return order, path