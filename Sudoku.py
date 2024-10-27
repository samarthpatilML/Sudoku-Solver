import tkinter as tk
import time
import json
import os

# Board data (0 represents empty cells)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with Scoreboard")
        
        self.cells = {}
        self.create_grid()
        
        # Buttons
        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.solve_button.grid(row=10, column=0, columnspan=3)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_board)
        self.reset_button.grid(row=10, column=3, columnspan=3)
        
        self.load_high_scores()
        self.score_label = tk.Label(root, text="High Score: " + str(self.high_score))
        self.score_label.grid(row=10, column=6, columnspan=3)

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                cell_value = sudoku_board[row][col]
                self.cells[(row, col)] = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                self.cells[(row, col)].grid(row=row, column=col, padx=5, pady=5)
                if cell_value != 0:
                    self.cells[(row, col)].insert(0, str(cell_value))
                    self.cells[(row, col)].config(state="readonly")

    def load_high_scores(self):
        # Load high scores from file
        if os.path.exists("high_score.json"):
            with open("high_score.json", "r") as file:
                self.high_score = json.load(file)
        else:
            self.high_score = float("inf")

    def save_high_scores(self, score):
        # Save high score if the current score is lower (faster)
        if score < self.high_score:
            self.high_score = score
            with open("high_score.json", "w") as file:
                json.dump(self.high_score, file)

    def get_board_values(self):
        # Read current values from the board
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.cells[(row, col)].get()
                current_row.append(int(value) if value else 0)
            board.append(current_row)
        return board

    def is_valid(self, board, num, pos):
        row, col = pos
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        # Check 3x3 grid
        grid_x, grid_y = (row // 3) * 3, (col // 3) * 3
        for i in range(grid_x, grid_x + 3):
            for j in range(grid_y, grid_y + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        # Backtracking method for solving the board
        empty = self.find_empty(board)
        if not empty:
            return True  # Puzzle solved
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].insert(0, str(num))
                self.cells[(row, col)].config(state="readonly")
                self.root.update()
                time.sleep(0.01)
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
                self.cells[(row, col)].config(state="normal")
                self.cells[(row, col)].delete(0, tk.END)
        return False

    def find_empty(self, board):
        # Find the next empty cell in the board
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve(self):
        # Start solving and measure time
        start_time = time.time()
        board = self.get_board_values()
        if self.solve_sudoku(board):
            end_time = time.time()
            score = round(end_time - start_time, 2)
            self.save_high_scores(score)
            self.score_label.config(text="High Score: " + str(self.high_score))
            tk.messagebox.showinfo("Solved!", f"Sudoku solved in {score} seconds!")
        else:
            tk.messagebox.showerror("Error", "No solution exists for this puzzle.")

    def reset_board(self):
        # Reset the board to the initial state
        for row in range(9):
            for col in range(9):
                cell = self.cells[(row, col)]
                cell.config(state="normal")
                cell.delete(0, tk.END)
                if sudoku_board[row][col] != 0:
                    cell.insert(0, str(sudoku_board[row][col]))
                    cell.config(state="readonly")

# Create the application
root = tk.Tk()
app = SudokuSolverApp(root)
root.mainloop()
