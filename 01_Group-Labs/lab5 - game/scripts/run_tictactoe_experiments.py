import sys
import os
import time
import math
import json
import numpy as np

os.environ['MPLCONFIGDIR'] = 'C:/Users/ACER/AppData/Local/Temp'
sys.path.append('01_Group-Labs/lab5 - game/lab05 - game')

from tictactoe import empty_board, actions, result, terminal, utility, other, show_board, random_player, play, check_board

np.random.seed(42)

results_data = {}

# ==============================================================================
# BÀI 1: Random vs Random 1000 games
# ==============================================================================
print("--- BÀI 1: Random vs Random ---")
start_time = time.time()
res_rnd = play(random_player, random_player, N=1000)
elapsed_rnd = time.time() - start_time
print(f"Random vs Random (1000 games): {res_rnd}, elapsed: {elapsed_rnd:.2f}s")
results_data['bai1_random_vs_random'] = {
    'results': res_rnd,
    'time_seconds': elapsed_rnd,
    'pct_x': res_rnd['x'] / 1000 * 100,
    'pct_o': res_rnd['o'] / 1000 * 100,
    'pct_d': res_rnd['d'] / 1000 * 100,
}

# ==============================================================================
# BÀI 2: AND-OR Tree Search
# ==============================================================================
print("\n--- BÀI 2: AND-OR Tree Search ---")

COUNT = 0
def results_and_or(state, action, player='x'):
    opponent = other(player)
    state = state.copy()
    state[action] = player
    o_actions = actions(state)
    if len(o_actions) < 1:
        return [state]
    r = []
    for o_a in o_actions:
        s = state.copy()
        s[o_a] = opponent
        r.append(s)
    return r

def and_or_search(state, player='x', draw_is_win=True):
    global COUNT
    COUNT = 0
    plan = or_search(state, player, draw_is_win)
    return plan, COUNT

def or_search(state, player, draw_is_win):
    global COUNT
    COUNT += 1
    u = utility(state, player)
    if u == -1 or (not draw_is_win and u == 0):
        return None
    for action in actions(state):
        plan = and_search(results_and_or(state, action, player), player, draw_is_win)
        if plan is not None:
            return [action, plan]
    return None

def and_search(states, player, draw_is_win):
    global COUNT
    COUNT += 1
    plans = []
    for s in states:
        u = utility(s, player)
        if u == 1:
            return "win"
        if draw_is_win and u == 0:
            return "draw"
        plan = or_search(s, player, draw_is_win)
        if plan is None:
            return None
        plans.append(['if', s, 'then', plan])
    return plans

# 4 Test Boards
# Case 1: X about to win
b1 = empty_board()
b1[0] = 'x'; b1[1] = 'o'; b1[3] = 'o'; b1[4] = 'x'

# Case 2: X can draw if it chooses 7
b2 = empty_board()
b2[0] = 'x'; b2[1] = 'o'; b2[2] = 'x'; b2[4] = 'o'

# Case 3: Bad situation
b3 = empty_board()
b3[0] = 'o'; b3[2] = 'x'; b3[8] = 'o'

# Case 4: Empty board
b4 = empty_board()

test_cases = {'case1_x_win': b1, 'case2_x_draw': b2, 'case3_bad_sit': b3, 'case4_empty': b4}

and_or_test_results = {}
for name, b in test_cases.items():
    # with draw_is_win = True
    t0 = time.time()
    plan_draw_win, c1 = and_or_search(b, 'x', draw_is_win=True)
    t_dw = time.time() - t0
    
    # with draw_is_win = False
    t0 = time.time()
    plan_win_only, c2 = and_or_search(b, 'x', draw_is_win=False)
    t_wo = time.time() - t0
    
    move_dw = plan_draw_win[0] if isinstance(plan_draw_win, list) else plan_draw_win
    move_wo = plan_win_only[0] if isinstance(plan_win_only, list) else plan_win_only
    
    and_or_test_results[name] = {
        'board': b,
        'draw_is_win': {'move': move_dw, 'nodes': c1, 'time': t_dw, 'has_plan': plan_draw_win is not None},
        'win_only': {'move': move_wo, 'nodes': c2, 'time': t_wo, 'has_plan': plan_win_only is not None}
    }
    print(f"AND-OR {name}: draw_is_win={move_dw} (nodes={c1}, {t_dw:.4f}s) | win_only={move_wo} (nodes={c2}, {t_wo:.4f}s)")

# AND-OR agent vs Random
def and_or_player(board, player='x'):
    plan, _ = and_or_search(board, player, draw_is_win=True)
    if plan is None or not isinstance(plan, list):
        return np.random.choice(actions(board))
    return plan[0]

t0 = time.time()
and_or_vs_rnd = play(and_or_player, random_player, N=100)
t_and_or_rnd = time.time() - t0
print(f"AND-OR vs Random (100 games): {and_or_vs_rnd}, time: {t_and_or_rnd:.2f}s")
results_data['bai2_and_or'] = {
    'test_cases': and_or_test_results,
    'vs_random': and_or_vs_rnd,
    'time_vs_random': t_and_or_rnd
}

# ==============================================================================
# BÀI 3: Minimax và Alpha-Beta Pruning
# ==============================================================================
print("\n--- BÀI 3: Minimax vs Alpha-Beta ---")

def minimax_search(board, player='x'):
    global COUNT
    COUNT = 0
    value, move = max_value(board, player)
    return {"move": move, "value": value, "nodes": COUNT}

def max_value(state, player):
    global COUNT
    COUNT += 1
    v = utility(state, player)
    if v is not None: return v, None
    v, move = -math.inf, None
    for a in actions(state):
        v2, _ = min_value(result(state, player, a), player)
        if v2 > v:
            v, move = v2, a
    return v, move

def min_value(state, player):
    global COUNT
    COUNT += 1
    v = utility(state, player)
    if v is not None: return v, None
    v, move = +math.inf, None
    for a in actions(state):
        v2, _ = max_value(result(state, other(player), a), player)
        if v2 < v:
            v, move = v2, a
    return v, move

def alpha_beta_search(board, player='x', action_fn=actions):
    global COUNT
    COUNT = 0
    value, move = max_value_ab(board, player, -math.inf, +math.inf, action_fn)
    return {"move": move, "value": value, "nodes": COUNT}

def max_value_ab(state, player, alpha, beta, action_fn):
    global COUNT
    COUNT += 1
    v = utility(state, player)
    if v is not None: return v, None
    v, move = -math.inf, None
    for a in action_fn(state):
        v2, _ = min_value_ab(result(state, player, a), player, alpha, beta, action_fn)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move

def min_value_ab(state, player, alpha, beta, action_fn):
    global COUNT
    COUNT += 1
    v = utility(state, player)
    if v is not None: return v, None
    v, move = +math.inf, None
    for a in action_fn(state):
        v2, _ = max_value_ab(result(state, other(player), a), player, alpha, beta, action_fn)
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move

def actions_ordered(board):
    acts = np.where(np.array(board) == ' ')[0].tolist()
    priority = [1, 0, 1,
                0, 2, 0,
                1, 0, 1]
    prios = [priority[i] for i in acts]
    return [a for _, a in sorted(zip(prios, acts), reverse=True)]

bai3_tests = {}
for name, b in test_cases.items():
    t0 = time.time()
    res_mm = minimax_search(b, 'x')
    t_mm = time.time() - t0
    res_mm['time'] = t_mm
    
    t0 = time.time()
    res_ab = alpha_beta_search(b, 'x', action_fn=actions)
    t_ab = time.time() - t0
    res_ab['time'] = t_ab
    
    t0 = time.time()
    res_abo = alpha_beta_search(b, 'x', action_fn=actions_ordered)
    t_abo = time.time() - t0
    res_abo['time'] = t_abo
    
    bai3_tests[name] = {
        'minimax': res_mm,
        'alpha_beta': res_ab,
        'alpha_beta_ordered': res_abo
    }
    print(f"TestCase {name}:")
    print(f"  Minimax: move={res_mm['move']}, val={res_mm['value']}, nodes={res_mm['nodes']}, time={t_mm:.4f}s")
    print(f"  AlphaBeta: move={res_ab['move']}, val={res_ab['value']}, nodes={res_ab['nodes']}, time={t_ab:.4f}s")
    print(f"  AB Ordered: move={res_abo['move']}, val={res_abo['value']}, nodes={res_abo['nodes']}, time={t_abo:.4f}s")

# AlphaBeta vs Random
def alpha_beta_player(board, player='x'):
    return alpha_beta_search(board, player, action_fn=actions_ordered)['move']

t0 = time.time()
ab_vs_rnd = play(alpha_beta_player, random_player, N=100)
t_ab_rnd = time.time() - t0
print(f"Alpha-Beta vs Random (100 games): {ab_vs_rnd}, time: {t_ab_rnd:.2f}s")

results_data['bai3_minimax_alphabeta'] = {
    'tests': bai3_tests,
    'vs_random': ab_vs_rnd,
    'time_vs_random': t_ab_rnd
}

# ==============================================================================
# BÀI 4: Heuristic Alpha-Beta
# ==============================================================================
print("\n--- BÀI 4: Heuristic Alpha-Beta ---")

def eval_fun(state, player='x'):
    u = utility(state, player)
    if u is not None: return u, True
    score = 0
    board = np.array(state).reshape((3, 3))
    diagonals = np.array([[board[i][i] for i in range(len(board))],
                          [board[i][len(board)-i-1] for i in range(len(board))]])
    for a_board in [board, np.transpose(board), diagonals]:
        for row in a_board:
            if sum(row == player) == 2 and any(row == ' '): score += .4
            if sum(row == other(player)) == 2 and any(row == ' '): score -= .4
    return score, False

def alpha_beta_cutoff_search(board, cutoff=None, player='x'):
    global COUNT
    COUNT = 0
    value, move = max_value_cutoff(board, player, -math.inf, +math.inf, depth=0, cutoff=cutoff)
    return {"move": move, "value": value, "nodes": COUNT}

def max_value_cutoff(state, player, alpha, beta, depth, cutoff):
    global COUNT
    COUNT += 1
    v, term = eval_fun(state, player)
    if term or (cutoff is not None and depth >= cutoff):
        return v, None
    v, move = -math.inf, None
    for a in actions(state):
        v2, _ = min_value_cutoff(result(state, player, a), player, alpha, beta, depth+1, cutoff)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move

def min_value_cutoff(state, player, alpha, beta, depth, cutoff):
    global COUNT
    COUNT += 1
    v, term = eval_fun(state, player)
    if term or (cutoff is not None and depth >= cutoff):
        return v, None
    v, move = +math.inf, None
    for a in actions(state):
        v2, _ = max_value_cutoff(result(state, other(player), a), player, alpha, beta, depth+1, cutoff)
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move

bai4_tests = {}
for name, b in test_cases.items():
    t0 = time.time()
    res_c2 = alpha_beta_cutoff_search(b, cutoff=2, player='x')
    t_c2 = time.time() - t0
    res_c2['time'] = t_c2
    
    t0 = time.time()
    res_c4 = alpha_beta_cutoff_search(b, cutoff=4, player='x')
    t_c4 = time.time() - t0
    res_c4['time'] = t_c4
    
    t0 = time.time()
    res_full = alpha_beta_cutoff_search(b, cutoff=None, player='x')
    t_full = time.time() - t0
    res_full['time'] = t_full
    
    bai4_tests[name] = {
        'cutoff_2': res_c2,
        'cutoff_4': res_c4,
        'full_ab': res_full
    }
    print(f"Heuristic {name}: C2={res_c2['move']} (nodes={res_c2['nodes']}, {t_c2:.4f}s) | C4={res_c4['move']} (nodes={res_c4['nodes']}, {t_c4:.4f}s) | Full={res_full['move']} (nodes={res_full['nodes']}, {t_full:.4f}s)")

def heuristic2_player(board, player='x'):
    return alpha_beta_cutoff_search(board, cutoff=2, player=player)['move']

def heuristic4_player(board, player='x'):
    return alpha_beta_cutoff_search(board, cutoff=4, player=player)['move']

t0 = time.time()
h2_vs_rnd = play(heuristic2_player, random_player, N=100)
t_h2_rnd = time.time() - t0

t0 = time.time()
h4_vs_rnd = play(heuristic4_player, random_player, N=100)
t_h4_rnd = time.time() - t0

# Heuristic vs AlphaBeta
h2_vs_ab = play(heuristic2_player, alpha_beta_player, N=1)
h4_vs_ab = play(heuristic4_player, alpha_beta_player, N=1)
h2_vs_h4 = play(heuristic2_player, heuristic4_player, N=1)

print(f"H2 vs Random: {h2_vs_rnd}, time={t_h2_rnd:.2f}s")
print(f"H4 vs Random: {h4_vs_rnd}, time={t_h4_rnd:.2f}s")
print(f"H2 vs AB: {h2_vs_ab}, H4 vs AB: {h4_vs_ab}, H2 vs H4: {h2_vs_h4}")

results_data['bai4_heuristic'] = {
    'tests': bai4_tests,
    'h2_vs_random': h2_vs_rnd,
    'h4_vs_random': h4_vs_rnd,
    'h2_vs_ab': h2_vs_ab,
    'h4_vs_ab': h4_vs_ab,
    'h2_vs_h4': h2_vs_h4
}

# ==============================================================================
# BÀI 5: Pure Monte Carlo Search (PMCS)
# ==============================================================================
print("\n--- BÀI 5: Pure Monte Carlo Search ---")

def playout(state, action, player='x'):
    state = result(state, player, action)
    curr = other(player)
    while True:
        u = utility(state, player)
        if u is not None:
            return u
        a = np.random.choice(actions(state))
        state = result(state, curr, a)
        curr = other(curr)

def playouts(board, action, player='x', N=100):
    return [playout(board, action, player) for _ in range(N)]

def pmcs(board, N=100, player='x'):
    acts = actions(board)
    n = max(1, math.floor(N / len(acts)))
    ps = {i: np.mean(playouts(board, i, player, N=n)) for i in acts}
    return max(ps, key=ps.get), ps

bai5_tests = {}
for name, b in test_cases.items():
    bai5_tests[name] = {}
    for N_sim in [10, 100, 1000]:
        t0 = time.time()
        best_a, ps = pmcs(b, N=N_sim, player='x')
        t_sim = time.time() - t0
        bai5_tests[name][f'N_{N_sim}'] = {
            'action': int(best_a),
            'utilities': {int(k): float(v) for k, v in ps.items()},
            'time': t_sim
        }
        print(f"PMCS {name} (N={N_sim}): best={best_a}, time={t_sim:.4f}s")

def pmcs10_player(board, player='x'):
    a, _ = pmcs(board, N=10, player=player)
    return a

def pmcs100_player(board, player='x'):
    a, _ = pmcs(board, N=100, player=player)
    return a

t0 = time.time()
pmcs10_vs_rnd = play(pmcs10_player, random_player, N=100)
t_pmcs10_rnd = time.time() - t0

t0 = time.time()
pmcs100_vs_rnd = play(pmcs100_player, random_player, N=100)
t_pmcs100_rnd = time.time() - t0

print(f"PMCS(10) vs Random: {pmcs10_vs_rnd}, time={t_pmcs10_rnd:.2f}s")
print(f"PMCS(100) vs Random: {pmcs100_vs_rnd}, time={t_pmcs100_rnd:.2f}s")

results_data['bai5_pmcs'] = {
    'tests': bai5_tests,
    'pmcs10_vs_random': pmcs10_vs_rnd,
    'pmcs100_vs_random': pmcs100_vs_rnd,
    'time_pmcs10': t_pmcs10_rnd,
    'time_pmcs100': t_pmcs100_rnd
}

# ==============================================================================
# BÀI 6: Monte Carlo Tree Search with UCB1
# ==============================================================================
print("\n--- BÀI 6: MCTS with UCB1 ---")

def UCT_depth1(board, N=100, player='x'):
    C = math.sqrt(2)
    acts = actions(board)
    u = [0.0] * len(acts)
    n = [0] * len(acts)
    n_parent = 0
    UCB1 = [+math.inf] * len(acts)
    
    for _ in range(N):
        action_id = UCB1.index(max(UCB1))
        p = playout(board, acts[action_id], player=player)
        u[action_id] += p
        n[action_id] += 1
        n_parent += 1
        for a_idx in range(len(acts)):
            if n[a_idx] > 0:
                UCB1[a_idx] = u[a_idx] / n[a_idx] + C * math.sqrt(math.log(n_parent) / n[a_idx])
    best_action = acts[n.index(max(n))]
    stats = {
        acts[i]: {'utility_sum': u[i], 'playouts': n[i], 'ucb1': UCB1[i], 'mean_val': u[i]/n[i] if n[i]>0 else 0}
        for i in range(len(acts))
    }
    return best_action, stats

bai6_tests = {}
for name, b in test_cases.items():
    bai6_tests[name] = {}
    for N_sim in [10, 100, 1000]:
        t0 = time.time()
        best_a, stats = UCT_depth1(b, N=N_sim, player='x')
        t_sim = time.time() - t0
        bai6_tests[name][f'N_{N_sim}'] = {
            'action': int(best_a),
            'stats': stats,
            'time': t_sim
        }
        print(f"UCB1 {name} (N={N_sim}): best={best_a}, time={t_sim:.4f}s")

def ucb1_10_player(board, player='x'):
    a, _ = UCT_depth1(board, N=10, player=player)
    return a

def ucb1_100_player(board, player='x'):
    a, _ = UCT_depth1(board, N=100, player=player)
    return a

t0 = time.time()
ucb1_10_vs_rnd = play(ucb1_10_player, random_player, N=100)
t_ucb1_10_rnd = time.time() - t0

t0 = time.time()
ucb1_100_vs_rnd = play(ucb1_100_player, random_player, N=100)
t_ucb1_100_rnd = time.time() - t0

print(f"UCB1(10) vs Random: {ucb1_10_vs_rnd}, time={t_ucb1_10_rnd:.2f}s")
print(f"UCB1(100) vs Random: {ucb1_100_vs_rnd}, time={t_ucb1_100_rnd:.2f}s")

results_data['bai6_ucb1'] = {
    'tests': bai6_tests,
    'ucb1_10_vs_random': ucb1_10_vs_rnd,
    'ucb1_100_vs_random': ucb1_100_vs_rnd,
    'time_ucb1_10': t_ucb1_10_rnd,
    'time_ucb1_100': t_ucb1_100_rnd
}

# ==============================================================================
# BÀI 7: Chơi tương tác (Simulated Interactive match trace)
# ==============================================================================
print("\n--- BÀI 7: Simulated Interactive Traces ---")

def simulate_interactive_match(agent_x, agent_o, name_x="Agent", name_o="Human"):
    board = empty_board()
    trace = []
    step = 1
    while True:
        # X move
        ax = agent_x(board, 'x')
        board = result(board, 'x', ax)
        w = check_board(board)
        trace.append({
            'step': step,
            'player': 'x',
            'actor': name_x,
            'action': int(ax),
            'board': list(board),
            'terminal': w != 'n',
            'winner': w if w != 'n' else None
        })
        if w != 'n':
            break
        step += 1
        
        # O move
        ao = agent_o(board, 'o')
        board = result(board, 'o', ao)
        w = check_board(board)
        trace.append({
            'step': step,
            'player': 'o',
            'actor': name_o,
            'action': int(ao),
            'board': list(board),
            'terminal': w != 'n',
            'winner': w if w != 'n' else None
        })
        if w != 'n':
            break
        step += 1
    return trace

# Match 1: Alpha-Beta (X) vs Heuristic / Random (O)
trace1 = simulate_interactive_match(alpha_beta_player, random_player, "AlphaBeta (Agent)", "Human (Simulated)")
# Match 2: Random (X) vs Alpha-Beta (O)
trace2 = simulate_interactive_match(random_player, alpha_beta_player, "Human (Simulated)", "AlphaBeta (Agent)")

results_data['bai7_interactive'] = {
    'match1_x_agent': trace1,
    'match2_o_agent': trace2
}

# Save all results to json
with open('tictactoe_results.json', 'w', encoding='utf-8') as f:
    json.dump(results_data, f, indent=2)

print("\n--- DONE ALL TICTACTOE EXPERIMENTS! Saved to tictactoe_results.json ---")
