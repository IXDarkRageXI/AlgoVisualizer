# main.py
import customtkinter as ctk
from maze import Maze
from Algo.BFS import bfs
from Algo.DFS import dfs
from Algo.AStar import astar
import time

CELL_SIZE = 25

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Visualizer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Algorithm Visualizer")
        self.geometry("1100x750")
        self.resizable(False, False)

        self.maze = Maze(21, 21)
        self.is_running = False

        self.configure(fg_color="#0f172a")  # modern dark navy

        self.create_layout()
        self.draw_maze()

    # =============================
    # UI LAYOUT
    # =============================

    def create_layout(self):

        # Title
        title = ctk.CTkLabel(
            self,
            text="Maze Algorithm Visualizer",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)

        # Main container
        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        self.canvas_frame.pack(side="left", padx=25, pady=25)

        self.canvas = ctk.CTkCanvas(
            self.canvas_frame,
            width=600,
            height=600,
            bg="#1e293b",
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        # Control Panel
        control_frame = ctk.CTkFrame(main_frame, width=300, corner_radius=15)
        control_frame.pack(side="right", padx=25, pady=25, fill="y")
        control_frame.pack_propagate(False)

        # Algorithm selector
        ctk.CTkLabel(
            control_frame,
            text="Algorithm",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))

        self.algo_selector = ctk.CTkSegmentedButton(
            control_frame,
            values=["BFS", "DFS", "A*"]
        )
        self.algo_selector.set("BFS")
        self.algo_selector.pack(pady=10)

        # Speed slider
        ctk.CTkLabel(
            control_frame,
            text="Animation Speed",
            font=ctk.CTkFont(size=16)
        ).pack(pady=(20, 5))

        self.speed_slider = ctk.CTkSlider(
            control_frame,
            from_=1,
            to=100
        )
        self.speed_slider.set(30)
        self.speed_slider.pack(pady=10)

        # Buttons
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="Start",
            height=40,
            corner_radius=12,
            command=self.start_visualization
        )
        self.start_btn.pack(pady=15)

        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="Reset",
            height=40,
            corner_radius=12,
            fg_color="#334155",
            hover_color="#475569",
            command=self.reset_visualization
        )
        self.reset_btn.pack(pady=10)

        self.new_maze_btn = ctk.CTkButton(
            control_frame,
            text="Generate New Maze",
            height=40,
            corner_radius=12,
            fg_color="#1d4ed8",
            hover_color="#2563eb",
            command=self.generate_new_maze
        )
        self.new_maze_btn.pack(pady=10)

        # Stats panel
        ctk.CTkLabel(
            control_frame,
            text="Statistics",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(30, 10))

        self.nodes_label = ctk.CTkLabel(control_frame, text="Nodes Explored: 0")
        self.nodes_label.pack(pady=5)

        self.path_label = ctk.CTkLabel(control_frame, text="Path Length: 0")
        self.path_label.pack(pady=5)

        self.time_label = ctk.CTkLabel(control_frame, text="Time: 0 ms")
        self.time_label.pack(pady=5)

    # =============================
    # DRAW MAZE
    # =============================

    def draw_maze(self):
        self.canvas.delete("all")

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):

                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = "#0f172a" if self.maze.grid[i][j] == 1 else "#1e293b"

                if (i, j) == self.maze.start:
                    color = "#22c55e"
                elif (i, j) == self.maze.end:
                    color = "#ef4444"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#0f172a"
                )

    # =============================
    # VISUALIZATION
    # =============================

    def start_visualization(self):
        if self.is_running:
            return

        self.is_running = True

        algo_name = self.algo_selector.get()

        start_time = time.time()

        if algo_name == "BFS":
            order, path = bfs(self.maze)
        elif algo_name == "DFS":
            order, path = dfs(self.maze)
        else:
            order, path = astar(self.maze)

        end_time = time.time()

        self.nodes_label.configure(text=f"Nodes Explored: {len(order)}")
        self.path_label.configure(text=f"Path Length: {len(path)}")
        self.time_label.configure(
            text=f"Time: {round((end_time-start_time)*1000,2)} ms"
        )

        self.animate(order, path)

    def animate(self, order, path):

        delay = int(101 - self.speed_slider.get())

        def draw_step(i):
            if i < len(order):
                x, y = order[i]
                if (x, y) not in [self.maze.start, self.maze.end]:
                    self.color_cell(x, y, "#3b82f6")
                self.after(delay, lambda: draw_step(i+1))
            else:
                self.draw_path(path)
                self.is_running = False

        draw_step(0)

    def draw_path(self, path):
        for x, y in path:
            if (x, y) not in [self.maze.start, self.maze.end]:
                self.color_cell(x, y, "#facc15")

    def color_cell(self, row, col, color):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline="#0f172a"
        )

    # =============================
    # CONTROLS
    # =============================

    def reset_visualization(self):
        if self.is_running:
            return
        self.draw_maze()
        self.nodes_label.configure(text="Nodes Explored: 0")
        self.path_label.configure(text="Path Length: 0")
        self.time_label.configure(text="Time: 0 ms")

    def generate_new_maze(self):
        if self.is_running:
            return
        self.maze.generate_maze()
        self.reset_visualization()


if __name__ == "__main__":
    app = Visualizer()
    app.mainloop()