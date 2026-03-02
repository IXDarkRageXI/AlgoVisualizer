import random

class Maze:
    def __init__(self, rows=21, cols=21):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.start = (1, 1)
        self.end = (rows - 2, cols - 2)
        self.generate_maze()

    def generate_maze(self):
        self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        def carve(x, y):
            directions = [(2,0), (-2,0), (0,2), (0,-2)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.rows-1 and 0 < ny < self.cols-1:
                    if self.grid[nx][ny] == 1:
                        self.grid[nx][ny] = 0
                        self.grid[x + dx//2][y + dy//2] = 0
                        carve(nx, ny)

        self.grid[1][1] = 0
        carve(1, 1)

        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)

    def reset(self):
        self.generate_maze()