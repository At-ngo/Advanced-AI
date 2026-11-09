import numpy as np
import time
import math
import json
import os

os.environ['MPLCONFIGDIR'] = 'C:/Users/ACER/AppData/Local/Temp'

from dots_and_boxes_test import empty_dots_board, actions_dots, result_dots, terminal_dots, utility_dots

np.random.seed(42)

dots_data = {}

# Problem Size Estimates
dots_data['problem_size'] = {
    '2x2_dots_1box': {'lines': 4, 'state_space': 2**4, 'game_tree': math.factorial(4)},
    '3x3_dots_4boxes': {'lines': 12, 'state_space': 2**12, 'game_tree': math.factorial(12)},
    '4x4_dots_9boxes': {'lines': 24, 'state_space': 2**24, 'game_tree': math.factorial(24)}
}

# 1000 games Random vs Random on 3x3 dots (4 boxes)
print("--- DOTS & BOXES: 1000 games Random vs Random on 3x3 dots ---", flush=True)
wins_dots = {1: 0, -1: 0, 0: 0}
t0 = time.time()
for _ in range(1000):
    b = empty_dots_board((3, 3))
    curr = 1
    while not terminal_dots(b):
        acts = actions_dots(b)
        a = acts[np.random.choice(len(acts))]
        b, curr, _ = result_dots(b, curr, a)
    u = utility_dots(b, 1)
    if u == 1.0: wins_dots[1] += 1
    elif u == -1.0: wins_dots[-1] += 1
    else: wins_dots[0] += 1
t_rnd_dots = time.time() - t0
print(f"Dots & Boxes 3x3 Random vs Random: {wins_dots} in {t_rnd_dots:.3f}s", flush=True)

dots_data['random_vs_random_3x3'] = {'results': wins_dots, 'time': t_rnd_dots}

# Minimax / Alpha-Beta with extra turn rule
DOTS_NODES = 0

def alphabeta_dots(b, player, root, alpha, beta):
    global DOTS_NODES
    DOTS_NODES += 1
    if terminal_dots(b):
        return utility_dots(b, root), None
        
    acts = actions_dots(b)
    best_m = None
    
    if player == root:
        best_v = -math.inf
        for a in acts:
            nb, next_p, _ = result_dots(b, player, a)
            v, _ = alphabeta_dots(nb, next_p, root, alpha, beta)
            if v > best_v:
                best_v = v
                best_m = a
                alpha = max(alpha, best_v)
            if best_v >= beta:
                break
        return best_v, best_m
    else:
        best_v = +math.inf
        for a in acts:
            nb, next_p, _ = result_dots(b, player, a)
            v, _ = alphabeta_dots(nb, next_p, root, alpha, beta)
            if v < best_v:
                best_v = v
                best_m = a
                beta = min(beta, best_v)
            if best_v <= alpha:
                break
        return best_v, best_m

# Test on 2x2 dots (1 box)
b22 = empty_dots_board((2, 2))
DOTS_NODES = 0; t0 = time.time()
v22, m22 = alphabeta_dots(b22, 1, 1, -math.inf, +math.inf)
t22 = time.time() - t0
print(f"2x2 Dots AB: val={v22}, move={m22}, nodes={DOTS_NODES}, time={t22:.4f}s", flush=True)

# Test on 3x3 dots (4 boxes)
b33 = empty_dots_board((3, 3))
DOTS_NODES = 0; t0 = time.time()
v33, m33 = alphabeta_dots(b33, 1, 1, -math.inf, +math.inf)
t33 = time.time() - t0
print(f"3x3 Dots AB: val={v33}, move={m33}, nodes={DOTS_NODES}, time={t33:.4f}s", flush=True)

dots_data['alphabeta_exact'] = {
    '2x2': {'val': v22, 'move': list(m22), 'nodes': DOTS_NODES, 'time': t22},
    '3x3': {'val': v33, 'move': list(m33), 'nodes': DOTS_NODES, 'time': t33}
}

with open('dots_results.json', 'w', encoding='utf-8') as f:
    json.dump(dots_data, f, indent=2)

print("--- DOTS & BOXES COMPLETE! Saved to dots_results.json ---", flush=True)
