import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import random

GRID_SIZE = 20
CELL_SIZE = 30
WIDTH     = GRID_SIZE * CELL_SIZE
HEIGHT    = GRID_SIZE * CELL_SIZE

COLOR_EMPTY   = "#F8F9FA"
COLOR_WALL    = "#212529"
COLOR_START   = "#2ECC71"
COLOR_END     = "#E74C3C"
COLOR_VISITED = "#5DADE2"
COLOR_PATH    = "#F1C40F"
COLOR_BORDER  = "#CED4DA"
COLOR_HOVER   = "#DEE2E6"

BG_ROOT   = "#FFFFFF"
BG_PANEL  = "#F1F3F5"
BG_STATUS = "#E9ECEF"


class PathfindingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinding Visualizer (BFS vs DFS)")
        self.root.config(bg=BG_ROOT)
        self.root.resizable(False, False)

        self.start_node = None
        self.end_node   = None
        self.mode       = "wall"
        self.is_running = False
        self.hover_cell = None
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        self.setup_ui()

    def setup_ui(self):
        top = tk.Frame(self.root, bg=BG_PANEL, pady=8, padx=10)
        top.pack(side=tk.TOP, fill=tk.X)

        row1 = tk.Frame(top, bg=BG_PANEL)
        row1.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row1, text="MODE:", font=("Segoe UI", 9, "bold"),
                 bg=BG_PANEL, fg="#495057").pack(side=tk.LEFT, padx=(0, 4))

        self.btn_start = tk.Button(
            row1, text="Set Start", width=9, cursor="hand2",
            bg="#2ECC71", fg="white", font=("Segoe UI", 9),
            relief=tk.RAISED, command=lambda: self.set_mode("start"))
        self.btn_start.pack(side=tk.LEFT, padx=2)

        self.btn_end = tk.Button(
            row1, text="Set End", width=9, cursor="hand2",
            bg="#E74C3C", fg="white", font=("Segoe UI", 9),
            relief=tk.RAISED, command=lambda: self.set_mode("end"))
        self.btn_end.pack(side=tk.LEFT, padx=2)

        self.btn_wall = tk.Button(
            row1, text="Set Wall", width=9, cursor="hand2",
            bg="#495057", fg="white", font=("Segoe UI", 9),
            relief=tk.SUNKEN, command=lambda: self.set_mode("wall"))
        self.btn_wall.pack(side=tk.LEFT, padx=2)

        tk.Frame(row1, width=2, bg=COLOR_BORDER).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(row1, text="ALGORITHM:", font=("Segoe UI", 9, "bold"),
                 bg=BG_PANEL, fg="#495057").pack(side=tk.LEFT, padx=(0, 4))

        self.algo_var = tk.StringVar(value="BFS")
        algo_box = ttk.Combobox(
            row1, textvariable=self.algo_var,
            values=["BFS", "DFS"], state="readonly",
            width=6, font=("Segoe UI", 9))
        algo_box.pack(side=tk.LEFT, padx=2)
        algo_box.bind("<<ComboboxSelected>>", lambda e: self.update_status_bar())

        tk.Frame(row1, width=2, bg=COLOR_BORDER).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(row1, text="SPEED:", font=("Segoe UI", 9, "bold"),
                 bg=BG_PANEL, fg="#495057").pack(side=tk.LEFT, padx=(0, 4))
        tk.Label(row1, text="Slow", font=("Segoe UI", 8),
                 bg=BG_PANEL, fg="#868E96").pack(side=tk.LEFT)

        self.speed_var = tk.IntVar(value=50)
        tk.Scale(
            row1, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.speed_var, length=110,
            showvalue=False, bg=BG_PANEL,
            highlightthickness=0, troughcolor=COLOR_BORDER,
            sliderrelief=tk.FLAT
        ).pack(side=tk.LEFT, padx=2)

        tk.Label(row1, text="Fast", font=("Segoe UI", 8),
                 bg=BG_PANEL, fg="#868E96").pack(side=tk.LEFT)

        row2 = tk.Frame(top, bg=BG_PANEL)
        row2.pack(fill=tk.X)

        btn_kw = {"font": ("Segoe UI", 9), "cursor": "hand2",
                  "relief": tk.FLAT, "padx": 10, "pady": 3}

        self.btn_run = tk.Button(
            row2, text="▶  Run", width=10,
            bg="#4263EB", fg="white",
            command=self.run_algorithm, **btn_kw)
        self.btn_run.pack(side=tk.LEFT, padx=2)

        tk.Button(
            row2, text="Random Maze",
            bg="#7950F2", fg="white",
            command=self.generate_random_maze, **btn_kw
        ).pack(side=tk.LEFT, padx=2)

        tk.Frame(row2, width=2, bg=COLOR_BORDER).pack(side=tk.LEFT, fill=tk.Y, padx=8)

        tk.Button(
            row2, text="Clear Path",
            bg="#74C0FC", fg="#1C1C1C",
            command=self.clear_path, **btn_kw
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            row2, text="Clear Walls",
            bg="#868E96", fg="white",
            command=self.clear_walls, **btn_kw
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            row2, text="Reset All",
            bg="#FA5252", fg="white",
            command=self.reset_all, **btn_kw
        ).pack(side=tk.LEFT, padx=2)

        self.stats_label = tk.Label(
            row2, text="", font=("Segoe UI", 9, "italic"),
            bg=BG_PANEL, fg="#495057")
        self.stats_label.pack(side=tk.RIGHT, padx=8)

        canvas_frame = tk.Frame(self.root, bg=COLOR_BORDER, padx=1, pady=1)
        canvas_frame.pack(padx=10, pady=(4, 4))

        self.canvas = tk.Canvas(
            canvas_frame, width=WIDTH, height=HEIGHT,
            bg=COLOR_EMPTY, highlightthickness=0)
        self.canvas.pack()

        self.draw_grid()

        status_bar = tk.Frame(self.root, bg=BG_STATUS, pady=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            status_bar,
            text="Mode: Place Walls  |  Algorithm: BFS  |  Status: Ready",
            font=("Segoe UI", 9), bg=BG_STATUS, fg="#495057", anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=12)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        self.canvas.bind("<Motion>", self.handle_hover)
        self.canvas.bind("<Leave>", self.handle_leave)

    def draw_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=COLOR_EMPTY, outline=COLOR_BORDER, width=1)
                self.grid[r][c] = {"rect": rect, "type": "empty"}

    def set_mode(self, mode):
        self.mode = mode
        for btn in (self.btn_start, self.btn_end, self.btn_wall):
            btn.config(relief=tk.RAISED)
        
        sink_map = {"start": self.btn_start, "end": self.btn_end, "wall": self.btn_wall}
        sink_map[mode].config(relief=tk.SUNKEN)
        self.update_status_bar()

    def handle_click(self, event):
        if self.is_running:
            return
        r, c = event.y // CELL_SIZE, event.x // CELL_SIZE
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            self.update_cell(r, c, toggle_wall=True)

    def handle_drag(self, event):
        if self.is_running:
            return
        if self.mode == "wall":
            r, c = event.y // CELL_SIZE, event.x // CELL_SIZE
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                self.update_cell(r, c, toggle_wall=False)

    def handle_hover(self, event):
        if self.is_running:
            return
        r, c = event.y // CELL_SIZE, event.x // CELL_SIZE
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            new_cell = (r, c)
            if new_cell != self.hover_cell:
                self.clear_hover()
                self.hover_cell = new_cell
                if self.grid[r][c]["type"] == "empty":
                    self.canvas.itemconfig(self.grid[r][c]["rect"], fill=COLOR_HOVER)
        else:
            self.clear_hover()

    def handle_leave(self, event):
        self.clear_hover()

    def clear_hover(self):
        if self.hover_cell:
            r, c = self.hover_cell
            if self.grid[r][c]["type"] == "empty":
                self.canvas.itemconfig(self.grid[r][c]["rect"], fill=COLOR_EMPTY)
            self.hover_cell = None

    def update_cell(self, r, c, toggle_wall=True):
        node = (r, c)

        if self.mode == "start":
            if self.start_node:
                self.set_cell_type(*self.start_node, "empty")
            self.start_node = node
            self.set_cell_type(r, c, "start")

        elif self.mode == "end":
            if self.end_node:
                self.set_cell_type(*self.end_node, "empty")
            self.end_node = node
            self.set_cell_type(r, c, "end")

        elif self.mode == "wall":
            if node != self.start_node and node != self.end_node:
                if toggle_wall:
                    new_type = "empty" if self.grid[r][c]["type"] == "wall" else "wall"
                else:
                    new_type = "wall"
                self.set_cell_type(r, c, new_type)

    def set_cell_type(self, r, c, cell_type):
        color_map = {
            "empty":   COLOR_EMPTY,
            "wall":    COLOR_WALL,
            "start":   COLOR_START,
            "end":     COLOR_END,
            "visited": COLOR_VISITED,
            "path":    COLOR_PATH,
        }
        self.grid[r][c]["type"] = cell_type
        self.canvas.itemconfig(self.grid[r][c]["rect"], fill=color_map[cell_type])

    def reset_all(self):
        if self.is_running:
            return
        self.start_node = None
        self.end_node = None
        self.stats_label.config(text="")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.set_cell_type(r, c, "empty")
        self.set_mode("wall")
        self.update_status_bar("Ready")

    def clear_path(self):
        if self.is_running:
            return
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]["type"] in ("visited", "path"):
                    self.set_cell_type(r, c, "empty")
        self.stats_label.config(text="")
        self.update_status_bar("Path Cleared")

    def clear_walls(self):
        if self.is_running:
            return
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]["type"] == "wall":
                    self.set_cell_type(r, c, "empty")
        self.update_status_bar("Walls Cleared")

    def generate_random_maze(self):
        if self.is_running:
            return
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in (self.start_node, self.end_node):
                    self.set_cell_type(r, c, "empty")
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in (self.start_node, self.end_node):
                    if random.random() < 0.30:
                        self.set_cell_type(r, c, "wall")
        self.stats_label.config(text="")
        self.update_status_bar("Random Maze Generated")

    def update_status_bar(self, status="Ready"):
        mode_names = {"start": "Place Start", "end": "Place End", "wall": "Place Walls"}
        self.status_label.config(
            text=f"Mode: {mode_names[self.mode]}  |  "
                 f"Algorithm: {self.algo_var.get()}  |  "
                 f"Status: {status}"
        )

    def get_delay(self):
        return max(5, 80 - int(self.speed_var.get() * 0.75))

    def set_running(self, running):
        self.is_running = running
        self.btn_run.config(state=tk.DISABLED if running else tk.NORMAL)

    def run_algorithm(self):
        if self.algo_var.get() == "BFS":
            self.run_bfs()
        else:
            self.run_dfs()

    def run_bfs(self):
        if not self.start_node or not self.end_node:
            messagebox.showwarning("Warning", "Please set both Start and End nodes first!")
            return

        self.clear_path()
        self.set_running(True)
        self.stats_label.config(text="")
        self.update_status_bar("Running BFS…")

        queue = deque([self.start_node])
        came_from = {self.start_node: None}
        found = False
        visited_count = 0
        delay = self.get_delay()

        while queue:
            current = queue.popleft()

            if current == self.end_node:
                found = True
                break

            r, c = current
            if current != self.start_node:
                self.set_cell_type(r, c, "visited")
                visited_count += 1
                self.root.update()
                self.root.after(delay)

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if (nr, nc) not in came_from and self.grid[nr][nc]["type"] != "wall":
                        came_from[(nr, nc)] = current
                        queue.append((nr, nc))

        if found:
            path_len = self.reconstruct_path(came_from)
            self.stats_label.config(text=f"Visited: {visited_count} nodes  |  Path length: {path_len}")
            self.update_status_bar("Finished — Path Found")
        else:
            self.update_status_bar("Finished — No Path Found")
            messagebox.showinfo("Result", "No path found!")

        self.set_running(False)

    def run_dfs(self):
        if not self.start_node or not self.end_node:
            messagebox.showwarning("Warning", "Please set both Start and End nodes first!")
            return

        self.clear_path()
        self.set_running(True)
        self.stats_label.config(text="")
        self.update_status_bar("Running DFS…")

        stack = [self.start_node]
        came_from = {self.start_node: None}
        found = False
        visited_count = 0
        delay = self.get_delay()

        while stack:
            current = stack.pop()

            if current == self.end_node:
                found = True
                break

            r, c = current
            if current != self.start_node:
                self.set_cell_type(r, c, "visited")
                visited_count += 1
                self.root.update()
                self.root.after(delay)

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if (nr, nc) not in came_from and self.grid[nr][nc]["type"] != "wall":
                        came_from[(nr, nc)] = current
                        stack.append((nr, nc))

        if found:
            path_len = self.reconstruct_path(came_from)
            self.stats_label.config(text=f"Visited: {visited_count} nodes  |  Path length: {path_len}")
            self.update_status_bar("Finished — Path Found")
        else:
            self.update_status_bar("Finished — No Path Found")
            messagebox.showinfo("Result", "No path found!")

        self.set_running(False)

    def reconstruct_path(self, came_from):
        current = self.end_node
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()

        delay = self.get_delay()
        for node in path:
            r, c = node
            if node != self.start_node and node != self.end_node:
                self.set_cell_type(r, c, "path")
                self.root.update()
                self.root.after(delay)

        return len(path)


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingVisualizer(root)
    root.mainloop()
