import tkinter as tk
from tkinter import messagebox
import chess

# Chess pieces Unicode characters
unicode_pieces = {
    'P': '\u2659', 'R': '\u2656', 'N': '\u2658', 'B': '\u2657', 'Q': '\u2655', 'K': '\u2654',
    'p': '\u265F', 'r': '\u265C', 'n': '\u265E', 'b': '\u265D', 'q': '\u265B', 'k': '\u265A'
}

# Initialize the board
board = chess.Board()

# Function to draw the chessboard
def draw_board(canvas):
    canvas.delete("all")
    colors = ["#f0d9b5", "#b58863"]  # Light and dark square colors
    for row in range(8):
        for col in range(8):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            color = colors[(row + col) % 2]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            # Add pieces using Unicode characters
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                canvas.create_text(x1 + square_size // 2, y1 + square_size // 2,
                                   text=unicode_pieces[piece.symbol()],
                                   font=("Arial", square_size // 2),
                                   tags="piece")

# Function to handle player's move
def on_click(event):
    global selected_square
    col = event.x // square_size
    row = 7 - (event.y // square_size)
    clicked_square = chess.square(col, row)

    if selected_square is None:
        if board.piece_at(clicked_square):
            selected_square = clicked_square
    else:
        move = chess.Move(selected_square, clicked_square)
        if move in board.legal_moves:
            board.push(move)
            draw_board(canvas)
            selected_square = None
            if not board.is_game_over():
                make_ai_move()
        else:
            selected_square = None

# Function for AI move
def make_ai_move():
    move = get_best_move(board, depth=3)
    board.push(move)
    draw_board(canvas)
    check_game_over()

# Check if the game is over
def check_game_over():
    if board.is_checkmate():
        if board.turn:
            messagebox.showinfo("Game Over", "Vedant Sonawane win wins!")
        else:
            messagebox.showinfo("Game Over", "You win!")
    elif board.is_stalemate():
        messagebox.showinfo("Game Over", "Draw by stalemate.")
    elif board.is_insufficient_material():
        messagebox.showinfo("Game Over", "Draw by insufficient material.")

# Evaluation function (simple material count)
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
    }
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0

    value = 0
    for piece_type, piece_value in piece_values.items():
        value += len(board.pieces(piece_type, chess.WHITE)) * piece_value
        value -= len(board.pieces(piece_type, chess.BLACK)) * piece_value
    return value

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to get the best move
def get_best_move(board, depth):
    best_move = None
    max_eval = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
            alpha = max(alpha, eval)

    return best_move

# Tkinter setup
root = tk.Tk()
root.title("Chess but moves form vedant Sonawane")

selected_square = None
square_size = 80
canvas = tk.Canvas(root, width=8*square_size, height=8*square_size)
canvas.pack()

canvas.bind("<Button-1>", on_click)
draw_board(canvas)

root.mainloop()

