import numpy as np
import time

def empty_board(shape=(6, 7)):
    return np.zeros(shape, dtype=np.int8)

def actions(board):
    return [c for c in range(board.shape[1]) if board[0, c] == 0]

def drop_piece(board, col, player):
    """Returns (new_board, row)"""
    new_b = board.copy()
    for r in range(board.shape[0]-1, -1, -1):
        if new_b[r, col] == 0:
            new_b[r, col] = player
            return new_b, r
    return None, -1

def check_win_fast(board, r, c, player, k=4):
    """Check win through (r, c) for player."""
    rows, cols = board.shape
    
    # Horizontal
    c_start = max(0, c - k + 1)
    c_end = min(cols - 1, c + k - 1)
    consecutive = 0
    for j in range(c_start, c_end + 1):
        if board[r, j] == player:
            consecutive += 1
            if consecutive >= k:
                return True
        else:
            consecutive = 0
            
    # Vertical (downwards only since piece is at top of col)
    if r + k <= rows:
        if all(board[r + i, c] == player for i in range(k)):
            return True
            
    # Diagonal \
    consecutive = 0
    d_start = max(-min(r, c), -k + 1)
    d_end = min(min(rows - 1 - r, cols - 1 - c), k - 1)
    for step in range(d_start, d_end + 1):
        if board[r + step, c + step] == player:
            consecutive += 1
            if consecutive >= k:
                return True
        else:
            consecutive = 0
            
    # Diagonal /
    consecutive = 0
    d_start = max(-min(rows - 1 - r, c), -k + 1)
    d_end = min(min(r, cols - 1 - c), k - 1)
    for step in range(d_start, d_end + 1):
        if board[r - step, c + step] == player:
            consecutive += 1
            if consecutive >= k:
                return True
        else:
            consecutive = 0
            
    return False

def check_board_win(board, player, k=4):
    rows, cols = board.shape
    for r in range(rows):
        for c in range(cols):
            if board[r, c] == player:
                # Horizontal
                if c + k <= cols and all(board[r, c+i] == player for i in range(k)):
                    return True
                # Vertical
                if r + k <= rows and all(board[r+i, c] == player for i in range(k)):
                    return True
                # Diagonal \
                if r + k <= rows and c + k <= cols and all(board[r+i, c+i] == player for i in range(k)):
                    return True
                # Diagonal /
                if r - k + 1 >= 0 and c + k <= cols and all(board[r-i, c+i] == player for i in range(k)):
                    return True
    return False

# Benchmark 1000 games of Random vs Random
t0 = time.time()
np.random.seed(42)
wins = {1: 0, -1: 0, 0: 0}
for _ in range(1000):
    b = empty_board((6, 7))
    curr = 1
    won = False
    for step in range(42):
        acts = actions(b)
        if not acts:
            wins[0] += 1
            won = True
            break
        col = np.random.choice(acts)
        b, r = drop_piece(b, col, curr)
        if check_win_fast(b, r, col, curr, 4):
            wins[curr] += 1
            won = True
            break
        curr = -curr
    if not won:
        wins[0] += 1

t1 = time.time()
print(f"1000 Random vs Random games completed in {t1 - t0:.3f}s: {wins}")
