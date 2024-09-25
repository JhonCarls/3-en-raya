import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

# Definir constantes
EMPTY = None
X = 'X'
O = 'O'

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("3 en Raya")
        self.root.geometry("400x500")
        
        # Cargar fondo GIF
        self.gif_label = tk.Label(self.root)
        self.gif_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_gif("fondo.gif")
        
        # Estado inicial (usando la función S0)
        self.S = self.S0()
        
        # Pantalla de menú
        self.show_menu()

    def load_gif(self, gif_path):
        # Cargar y reproducir fondo GIF
        self.gif_image = Image.open(gif_path)
        self.frames = [ImageTk.PhotoImage(img.copy()) for img in ImageSequence.Iterator(self.gif_image)]
        self.frame_idx = 0
        self.update_gif()

    def update_gif(self):
        frame = self.frames[self.frame_idx]
        self.gif_label.configure(image=frame)
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.root.after(100, self.update_gif)

    def show_menu(self):
        # Pantalla de inicio con opciones
        self.clear_window()
        label = tk.Label(self.root, text="Modo de Juego", font=("Arial", 20), bg="white")
        label.pack(pady=20)

        button_1player = tk.Button(self.root, text="1 Jugador", font=("Arial", 16), command=self.start_1player)
        button_1player.pack(pady=10)

        button_2players = tk.Button(self.root, text="2 Jugadores", font=("Arial", 16), command=self.start_2players)
        button_2players.pack(pady=10)

    def clear_window(self):
        # Limpiar la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()
        self.gif_label = tk.Label(self.root)
        self.gif_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_gif("fondo.gif")

    def start_1player(self):
        self.clear_window()
        self.single_player = True
        self.current_player = X
        self.S = self.S0()  # Reiniciar tablero con estado inicial
        self.play_game()

    def start_2players(self):
        self.clear_window()
        self.single_player = False
        self.current_player = X
        self.S = self.S0()  # Reiniciar tablero con estado inicial
        self.play_game()

    def play_game(self):
        # Mostrar el tablero y gestionar los turnos
        self.board_buttons = []
        self.show_board()

    def show_board(self):
        self.turn_label = tk.Label(self.root, text=f"Turno: {self.current_player}", font=("Arial", 16), bg="white")
        self.turn_label.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(frame, text="", font=("Arial", 24), width=5, height=2, 
                                    command=lambda r=i, c=j: self.make_move(r, c))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.board_buttons.append(row)

    def make_move(self, row, col):
        if self.S[row][col] == EMPTY:
            self.S[row][col] = self.current_player
            self.board_buttons[row][col].config(text=self.current_player)

            if self.TERMINAL(self.S):
                self.show_result(f"¡{self.current_player} ha ganado!", f"imagen{1 if self.current_player == X else 2}.gif")
            elif not any(EMPTY in row for row in self.S):
                self.show_result("Es un empate.", "imagen3.gif")
            else:
                self.current_player = O if self.current_player == X else X
                self.update_turn_label()

                if self.single_player and self.current_player == O:
                    self.root.after(100, self.computer_move)

    def update_turn_label(self):
        self.turn_label.config(text=f"Turno: {self.current_player}")

    def check_winner(self, board):
        # Verificar filas, columnas y diagonales
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
                return True
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
                return True
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return True
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return True
        return False

    def computer_move(self):
        _, best_move = self.minimax(self.S, True)
        if best_move:
            row, col = best_move
            self.make_move(row, col)

    def minimax(self, board, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if self.TERMINAL(board):
            return (self.UTILITY(board), None)
        elif not any(EMPTY in row for row in board):
            return 0, None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for action in self.ACTIONS(board):
                new_board = self.RESULT(board, action)
                eval, _ = self.minimax(new_board, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for action in self.ACTIONS(board):
                new_board = self.RESULT(board, action)
                eval, _ = self.minimax(new_board, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = action
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def ACTIONS(self, board):
        actions = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    actions.append((i, j))
        return actions

    def RESULT(self, board, action):
        new_board = [row[:] for row in board]
        i, j = action
        new_board[i][j] = self.current_player
        return new_board

    def S0(self):
        # Estado inicial del tablero
        return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

    def TERMINAL(self, s):
        # Verifica si el estado s es terminal
        return self.check_winner(s) or not any(EMPTY in row for row in s)

    def UTILITY(self, s):
        # Valor final del estado terminal
        if self.check_winner(s):
            return 1 if self.current_player == X else -1
        return 0

    def show_result(self, result_text, gif_path):
        self.clear_window()
        self.load_gif(gif_path)

        label = tk.Label(self.root, text=result_text, font=("Arial", 24), bg="white")
        label.pack(pady=20)

        label = tk.Label(self.root, text="¿Quieres jugar otra vez?", font=("Arial", 20), bg="white")
        label.pack(pady=15)

        button_yes = tk.Button(self.root, text="Sí", font=("Arial", 16), command=self.reset_game)
        button_yes.pack(pady=10)

        button_no = tk.Button(self.root, text="No", font=("Arial", 16), command=self.root.quit)
        button_no.pack(pady=10)

    def reset_game(self):
        self.S = self.S0()
        self.current_player = X
        self.clear_window()
        self.show_menu()

# Crear ventana principal
root = tk.Tk()
game = TicTacToeGame(root)
root.mainloop()
