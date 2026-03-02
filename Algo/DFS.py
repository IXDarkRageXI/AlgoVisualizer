def dfs(maze):
    rows, cols = maze.rows, maze.cols
    start, end = maze.start, maze.end
    grid = maze.grid

    stack = [start]
    visited = {start}
    parent = {}
    order = []

    while stack:
        current = stack.pop()
        order.append(current)

        if current == end:
            break

        x, y = current
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and
                grid[nx][ny] == 0 and (nx, ny) not in visited):
                stack.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

    path = []
    node = end
    while node in parent:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()

    return order, path