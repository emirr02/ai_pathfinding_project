import tkinter as tk
from tkinter import messagebox
from collections import deque

# Constants
GRID_SIZE = 20
CELL_SIZE = 30
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Colors
COLOR_EMPTY = "white"
COLOR_WALL = "black"
COLOR_START = "green"
COLOR_END = "red"
COLOR_VISITED = "lightblue"
COLOR_PATH = "yellow"
COLOR_BORDER = "gray"

class PathfindingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinding Visualizer - Phase 2")
        
        # Application State
        self.start_node = None
        self.end_node = None
        self.mode = "wall"  # Options: start, end, wall
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        self.setup_ui()

    def setup_ui(self):
        # Control Panel
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_start = tk.Button(control_frame, text="Set Start", command=lambda: self.set_mode("start"))
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_end = tk.Button(control_frame, text="Set End", command=lambda: self.set_mode("end"))
        self.btn_end.pack(side=tk.LEFT, padx=5)

        self.btn_wall = tk.Button(control_frame, text="Set Wall", command=lambda: self.set_mode("wall"), relief=tk.SUNKEN)
        self.btn_wall.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Reset", command=self.reset_all).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Clear Path", command=self.clear_path).pack(side=tk.LEFT, padx=5)
        
        # Algorithm Buttons
        tk.Button(control_frame, text="Run BFS", bg="lightgreen", command=self.run_bfs).pack(side=tk.RIGHT, padx=5)
        tk.Button(control_frame, text="Run DFS", bg="lightcyan", command=self.run_dfs).pack(side=tk.RIGHT, padx=5)

        # Status Label
        self.status_label = tk.Label(self.root, text="Mode: Set Walls", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.TOP)

        # Canvas for the Grid
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=COLOR_EMPTY)
        self.canvas.pack(pady=10, padx=10)

        self.draw_grid()

        # Bindings
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)

    def draw_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_EMPTY, outline=COLOR_BORDER)
                self.grid[r][c] = {"rect": rect, "type": "empty"}

    def set_mode(self, mode):
        self.mode = mode
        # Update button appearance
        self.btn_start.config(relief=tk.RAISED)
        self.btn_end.config(relief=tk.RAISED)
        self.btn_wall.config(relief=tk.RAISED)

        if mode == "start":
            self.btn_start.config(relief=tk.SUNKEN)
            self.status_label.config(text="Mode: Place Start Node")
        elif mode == "end":
            self.btn_end.config(relief=tk.SUNKEN)
            self.status_label.config(text="Mode: Place End Node")
        elif mode == "wall":
            self.btn_wall.config(relief=tk.SUNKEN)
            self.status_label.config(text="Mode: Place Walls")

    def handle_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.update_cell(row, col)

    def handle_drag(self, event):
        if self.mode == "wall":
            row = event.y // CELL_SIZE
            col = event.x // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.update_cell(row, col)

    def update_cell(self, r, c):
        current_node = (r, c)
        
        if self.mode == "start":
            if self.start_node:
                old_r, old_c = self.start_node
                self.set_cell_type(old_r, old_c, "empty")
            self.start_node = current_node
            self.set_cell_type(r, c, "start")
        
        elif self.mode == "end":
            if self.end_node:
                old_r, old_c = self.end_node
                self.set_cell_type(old_r, old_c, "empty")
            self.end_node = current_node
            self.set_cell_type(r, c, "end")
            
        elif self.mode == "wall":
            if current_node != self.start_node and current_node != self.end_node:
                # Toggle wall if clicked, but handle_drag usually just sets it
                new_type = "empty" if self.grid[r][c]["type"] == "wall" else "wall"
                self.set_cell_type(r, c, "wall")

    def set_cell_type(self, r, c, cell_type):
        color_map = {
            "empty": COLOR_EMPTY,
            "wall": COLOR_WALL,
            "start": COLOR_START,
            "end": COLOR_END,
            "visited": COLOR_VISITED,
            "path": COLOR_PATH
        }
        self.grid[r][c]["type"] = cell_type
        self.canvas.itemconfig(self.grid[r][c]["rect"], fill=color_map[cell_type])

    def reset_all(self):
        self.start_node = None
        self.end_node = None
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.set_cell_type(r, c, "empty")
        self.status_label.config(text="Grid Reset. Mode: Set Walls")
        self.set_mode("wall")

    def clear_path(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]["type"] in ["visited", "path"]:
                    self.set_cell_type(r, c, "empty")
        self.status_label.config(text="Path Cleared. Modes and Walls Preserved.")

    def run_bfs(self):
        if not self.start_node or not self.end_node:
            messagebox.showwarning("Warning", "Please set both Start and End nodes first!")
            return

        self.clear_path()

        queue = deque([self.start_node])
        came_from = {self.start_node: None}
        found = False

        while queue:
            current = queue.popleft()
            
            if current == self.end_node:
                found = True
                break
            
            r, c = current
            if current != self.start_node:
                self.set_cell_type(r, c, "visited")
                self.root.update() 
                self.root.after(10) 

            # BFS Explores neighbors level by level
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if (nr, nc) not in came_from and self.grid[nr][nc]["type"] != "wall":
                        came_from[(nr, nc)] = current
                        queue.append((nr, nc))

        if found:
            self.reconstruct_path(came_from)
        else:
            messagebox.showinfo("Result", "No path found using BFS!")

    def run_dfs(self):
        if not self.start_node or not self.end_node:
            messagebox.showwarning("Warning", "Please set both Start and End nodes first!")
            return

        self.clear_path()

        stack = [self.start_node]
        came_from = {self.start_node: None}
        found = False

        while stack:
            current = stack.pop()
            
            if current == self.end_node:
                found = True
                break
            
            r, c = current
            if current != self.start_node:
                self.set_cell_type(r, c, "visited")
                self.root.update()
                self.root.after(10)

            # DFS explores neighbors deep into one branch (LIFO)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if (nr, nc) not in came_from and self.grid[nr][nc]["type"] != "wall":
                        came_from[(nr, nc)] = current
                        stack.append((nr, nc))

        if found:
            self.reconstruct_path(came_from)
        else:
            messagebox.showinfo("Result", "No path found using DFS!")

    def reconstruct_path(self, came_from):
        current = self.end_node
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        
        path.reverse()
        for node in path:
            r, c = node
            if node != self.start_node and node != self.end_node:
                self.set_cell_type(r, c, "path")
                self.root.update()
                self.root.after(20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingVisualizer(root)
    root.mainloop()
