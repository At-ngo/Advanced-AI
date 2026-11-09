import numpy as np
import time
import math
import json

def empty_dots_board(shape=(3, 3)):
    """shape is (rows, cols) of dots. Boxes is (rows-1, cols-1)."""
    return {
        'size': shape,
        'lines': {},
        'boxes': {}
    }

def actions_dots(board):
    r_max, c_max = board['size']
    acts = []
    # Horizontal lines: r in 0..r_max-1, c in 0..c_max-2
    for r in range(r_max):
        for c in range(c_max - 1):
            if ('h', r, c) not in board['lines']:
                acts.append(('h', r, c))
    # Vertical lines: r in 0..r_max-2, c in 0..c_max-1
    for r in range(r_max - 1):
        for c in range(c_max):
            if ('v', r, c) not in board['lines']:
                acts.append(('v', r, c))
    return acts

def result_dots(board, player, action):
    new_b = {
        'size': board['size'],
        'lines': board['lines'].copy(),
        'boxes': board['boxes'].copy()
    }
    new_b['lines'][action] = player
    
    # Check if any box completed
    ori, r, c = action
    boxes_completed = 0
    
    def is_box_closed(b_r, b_c, lines):
        # 4 edges of box (b_r, b_c)
        top = ('h', b_r, b_c)
        bot = ('h', b_r + 1, b_c)
        left = ('v', b_r, b_c)
        right = ('v', b_r, b_c + 1)
        return (top in lines) and (bot in lines) and (left in lines) and (right in lines)
        
    candidates = []
    if ori == 'h':
        # Box above (r-1, c) and box below (r, c)
        if r > 0: candidates.append((r - 1, c))
        if r < board['size'][0] - 1: candidates.append((r, c))
    else: # 'v'
        # Box left (r, c-1) and box right (r, c)
        if c > 0: candidates.append((r, c - 1))
        if c < board['size'][1] - 1: candidates.append((r, c))
        
    for b_r, b_c in candidates:
        if (b_r, b_c) not in new_b['boxes']:
            if is_box_closed(b_r, b_c, new_b['lines']):
                new_b['boxes'][(b_r, b_c)] = player
                boxes_completed += 1
                
    # Next player: if box completed, same player goes again; else opponent
    next_player = player if boxes_completed > 0 else -player
    return new_b, next_player, boxes_completed

def terminal_dots(board):
    total_boxes = (board['size'][0] - 1) * (board['size'][1] - 1)
    return len(board['boxes']) == total_boxes

def utility_dots(board, player=1):
    total_boxes = (board['size'][0] - 1) * (board['size'][1] - 1)
    if len(board['boxes']) < total_boxes:
        return None
    p1 = sum(1 for v in board['boxes'].values() if v == player)
    p2 = sum(1 for v in board['boxes'].values() if v == -player)
    if p1 > p2: return 1.0
    if p1 < p2: return -1.0
    return 0.0

# Test on 2x2 dots (1 box) and 3x3 dots (4 boxes)
b22 = empty_dots_board((2, 2))
print("Actions 2x2:", actions_dots(b22))

b33 = empty_dots_board((3, 3))
print("Actions 3x3 count:", len(actions_dots(b33)))
