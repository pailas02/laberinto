import csv
import tkinter as tk
from tkinter import filedialog
from colorama import Fore, Style  # Importar colores de colorama

class MazeSolver:
    def __init__(self):
        self.paths = []

    def find_start_end(self, maze):
        rows = len(maze)
        cols = len(maze[0])
        start = None
        end = None

        for x in range(cols):
            if maze[0][x] == 0:
                start = (x, 0)
            if maze[rows - 1][x] == 0:
                end = (x, rows - 1)

        for y in range(1, rows - 1):
            if maze[y][0] == 0:
                start = (0, y)
            if maze[y][cols - 1] == 0:
                end = (cols - 1, y)

        return start, end

    def solve(self, maze, startX, startY, endX, endY, path=[]):
        rows = len(maze)
        cols = len(maze[0])

        if (
            startX < 0 or startX >= cols or
            startY < 0 or startY >= rows or
            maze[startY][startX] == 1
        ):
            return

        path.append((startX, startY))

        if startX == endX and startY == endY:
            self.paths.append(list(path))
            path.pop()
            return

        maze[startY][startX] = 1

        self.solve(maze, startX + 1, startY, endX, endY, path)
        self.solve(maze, startX - 1, startY, endX, endY, path)
        self.solve(maze, startX, startY + 1, endX, endY, path)
        self.solve(maze, startX, startY - 1, endX, endY, path)

        maze[startY][startX] = 0
        path.pop()

    def display_solution(self, path, maze):
        for x, y in path:
            maze[y][x] = 2

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Laberinto Solver")

        self.laberinto = None
        self.solver = MazeSolver()
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Cargar Laberinto", command=self.load_maze)
        self.load_button.pack()

        self.solve_button = tk.Button(root, text="Resolver Laberinto", command=self.solve_maze)
        self.solve_button.pack()

        self.show_solution_button = tk.Button(root, text="Mostrar Solución", command=self.show_solution)
        self.show_solution_button.pack()

        self.solution_index = 0

    def load_maze(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.laberinto = cargar_laberinto(file_path)
            self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        cell_size = 20
        for y, row in enumerate(self.laberinto):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.canvas.create_rectangle(x * cell_size, y * cell_size,
                                                 (x + 1) * cell_size, (y + 1) * cell_size,
                                                 fill="black")
                elif cell == 0:
                    self.canvas.create_rectangle(x * cell_size, y * cell_size,
                                                 (x + 1) * cell_size, (y + 1) * cell_size,
                                                 fill="yellow")

    def solve_maze(self):
        if self.laberinto:
            start, end = self.solver.find_start_end(self.laberinto)
            startX, startY = start
            endX, endY = end

            self.solver.solve(self.laberinto, startX, startY, endX, endY, [])  # Se pasa una lista vacía como argumento

    def show_solution(self):
        if self.laberinto and self.solver.paths:
            path = self.solver.paths[self.solution_index]
            laberinto_copy = [row[:] for row in self.laberinto]
            self.solver.display_solution(path, laberinto_copy)
            self.draw_maze()
            
            # Mostrar la solución en la consola con colores
            print(Fore.GREEN + "Ruta {}:".format(self.solution_index + 1))
            for row in laberinto_copy:
                for cell in row:
                    if cell == 1:
                        print(Fore.BLACK + "#" + Style.RESET_ALL, end=" ")
                    elif cell == 2:
                        print(Fore.YELLOW + "#" + Style.RESET_ALL, end=" ")
                    else:
                        print(cell, end=" ")
                print()

            self.solution_index += 1
            if self.solution_index >= len(self.solver.paths):
                self.solution_index = 0

def cargar_laberinto(matriz):
    laberinto = []
    with open(matriz, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            laberinto.append(list(map(int, fila)))
    return laberinto

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()
