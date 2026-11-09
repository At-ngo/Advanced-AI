import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import math

os.environ['MPLCONFIGDIR'] = 'C:/Users/ACER/AppData/Local/Temp'

script_dir = os.path.dirname(os.path.abspath(__file__))
report_dir = os.path.dirname(script_dir)
img_dir = os.path.join(report_dir, 'img')
os.makedirs(img_dir, exist_ok=True)

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'font.sans-serif': ['DejaVu Sans', 'Arial'],
    'font.family': 'sans-serif'
})

# Load node results from JSON (verified identical across all runs)
with open(os.path.join(script_dir, 'tictactoe_results.json'), 'r', encoding='utf-8') as f:
    ttt_data = json.load(f)

# ==============================================================================
# FIGURE 1: Tic-Tac-Toe Win/Draw/Loss comparison vs Random (Executed Notebooks)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

agents = ['Random', 'AND-OR', 'Alpha-Beta', 'Heuristic C=2', 'Heuristic C=4', 'PMCS (N=10)', 'PMCS (N=100)', 'UCB1 (N=10)', 'UCB1 (N=100)']
wins   = [59.0, 96.0, 94.0, 96.0, 99.0, 92.0, 98.0, 86.0, 97.0]
draws  = [12.6,  4.0,  6.0,  4.0,  1.0,  2.0,  1.0,  5.0,  3.0]
losses = [28.4,  0.0,  0.0,  0.0,  0.0,  6.0,  1.0,  9.0,  0.0]

x = np.arange(len(agents))
width = 0.55

p1 = ax.bar(x, wins, width, label='Thắng (Win %)', color='#2ca02c')
p2 = ax.bar(x, draws, width, bottom=wins, label='Hòa (Draw %)', color='#1f77b4')
p3 = ax.bar(x, losses, width, bottom=np.array(wins) + np.array(draws), label='Thua (Loss %)', color='#d62728')

ax.set_ylabel('Tỷ lệ phần trăm (%)')
ax.set_title('So sánh kết quả đối đầu của các tác tử Tic-Tac-Toe với Random Player (100 ván)')
ax.set_xticks(x)
ax.set_xticklabels(agents, rotation=25, ha='right')
ax.legend(loc='lower left')
ax.set_ylim(0, 105)
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
fig1_path = os.path.join(img_dir, 'fig_tictactoe_winrates.png')
plt.savefig(fig1_path)
plt.close()
print(f"Saved {fig1_path}")

# ==============================================================================
# FIGURE 2: Node Complexity Comparison (Log scale)
# ==============================================================================
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

cases = ['X sắp thắng\n(Case 1)', 'X tìm đường hòa\n(Case 2)', 'Thế cờ bất lợi\n(Case 3)', 'Bàn cờ rỗng\n(Case 4)']
nodes_mm = [
    ttt_data['bai3_minimax_alphabeta']['tests']['case1_x_win']['minimax']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case2_x_draw']['minimax']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case3_bad_sit']['minimax']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case4_empty']['minimax']['nodes']
]
nodes_ab = [
    ttt_data['bai3_minimax_alphabeta']['tests']['case1_x_win']['alpha_beta']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case2_x_draw']['alpha_beta']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case3_bad_sit']['alpha_beta']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case4_empty']['alpha_beta']['nodes']
]
nodes_abo = [
    ttt_data['bai3_minimax_alphabeta']['tests']['case1_x_win']['alpha_beta_ordered']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case2_x_draw']['alpha_beta_ordered']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case3_bad_sit']['alpha_beta_ordered']['nodes'],
    ttt_data['bai3_minimax_alphabeta']['tests']['case4_empty']['alpha_beta_ordered']['nodes']
]
nodes_h4 = [
    ttt_data['bai4_heuristic']['tests']['case1_x_win']['cutoff_4']['nodes'],
    ttt_data['bai4_heuristic']['tests']['case2_x_draw']['cutoff_4']['nodes'],
    ttt_data['bai4_heuristic']['tests']['case3_bad_sit']['cutoff_4']['nodes'],
    ttt_data['bai4_heuristic']['tests']['case4_empty']['cutoff_4']['nodes']
]

x = np.arange(len(cases))
w = 0.18

ax.bar(x - 1.5*w, nodes_mm, w, label='Minimax đệ quy', color='#e377c2')
ax.bar(x - 0.5*w, nodes_ab, w, label='Alpha-Beta Pruning', color='#ff7f0e')
ax.bar(x + 0.5*w, nodes_abo, w, label='Alpha-Beta + Move Ordering', color='#1f77b4')
ax.bar(x + 1.5*w, nodes_h4, w, label='Heuristic (Cutoff=4)', color='#2ca02c')

ax.set_yscale('log')
ax.set_ylabel('Số nút duyệt (Log scale)')
ax.set_title('Hiệu quả giảm không gian tìm kiếm giữa các thuật toán trên Tic-Tac-Toe')
ax.set_xticks(x)
ax.set_xticklabels(cases)
ax.legend(loc='upper left')
ax.grid(True, which='both', linestyle='--', alpha=0.4)

plt.tight_layout()
fig2_path = os.path.join(img_dir, 'fig_node_complexity.png')
plt.savefig(fig2_path)
plt.close()
print(f"Saved {fig2_path}")

# ==============================================================================
# FIGURE 3: Connect 4 Combinatorial Explosion & Scale (Executed Notebook Data)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=300)

board_names = ['3x3 (k=3)', '3x4 (k=3)', '4x4 (k=4)']
# Node counts (from assignment_connect4.ipynb cells [25] & [27])
mm_c4_nodes = [1721, 62599, 10000000]  # 4x4 Minimax timeout (>10^7)
ab_c4_nodes = [376, 599, 50956]        # Alpha-Beta mặc định [0..C-1]
abo_c4_nodes = [374, 510, 127971]      # Alpha-Beta Center-first

x = np.arange(len(board_names))
w = 0.25

ax1.bar(x - w, mm_c4_nodes, w, label='Minimax (4x4 > 10^7)', color='#d62728')
ax1.bar(x,     ab_c4_nodes, w, label='Alpha-Beta (mặc định)', color='#2ca02c')
ax1.bar(x + w, abo_c4_nodes, w, label='AB Center-first', color='#1f77b4')
ax1.set_yscale('log')
ax1.set_ylabel('Số nút duyệt (Log scale)')
ax1.set_title('Số nút duyệt theo kích thước bàn cờ Connect 4')
ax1.set_xticks(x)
ax1.set_xticklabels(board_names)
ax1.legend()
ax1.grid(True, which='both', linestyle='--', alpha=0.4)

# Runtime (from assignment_connect4.ipynb cells [25] & [27])
mm_times  = [0.008, 0.4253, 60.0]
ab_times  = [0.0070, 0.0069, 0.6042]
abo_times = [0.0069, 0.0127, 1.9690]

ax2.bar(x - w, mm_times, w, label='Minimax (4x4 > 60s)', color='#d62728')
ax2.bar(x,     ab_times, w, label='Alpha-Beta (mặc định)', color='#2ca02c')
ax2.bar(x + w, abo_times, w, label='AB Center-first', color='#1f77b4')
ax2.set_yscale('log')
ax2.set_ylabel('Thời gian thực thi (giây, Log scale)')
ax2.set_title('Thời gian tính toán nước đi đầu tiên')
ax2.set_xticks(x)
ax2.set_xticklabels(board_names)
ax2.legend()
ax2.grid(True, which='both', linestyle='--', alpha=0.4)

plt.tight_layout()
fig3_path = os.path.join(img_dir, 'fig_c4_scaling.png')
plt.savefig(fig3_path)
plt.close()
print(f"Saved {fig3_path}")

# ==============================================================================
# FIGURE 4: Connect 4 Opening First Move Heuristic Values
# ==============================================================================
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

cols = [0, 1, 2, 3, 4, 5, 6]
scores = [-18, -14, 0, 0, 0, -14, -18] # from our experiment
# Window potential for each column
potential_lines = [3, 4, 7, 14, 7, 4, 3]

color_map = ['#e74c3c' if s < 0 else '#2ecc71' for s in scores]
bars = ax.bar(cols, potential_lines, color='#3498db', alpha=0.8, edgecolor='black', width=0.55)
# Add potential line count annotations
for b, pl, sc in zip(bars, potential_lines, scores):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3, f"{pl} chuỗi", ha='center', va='bottom', fontweight='bold', fontsize=9)

ax.set_xlabel('Cột lựa chọn nước đi đầu tiên (Column Index)')
ax.set_ylabel('Số chuỗi 4-ô tiềm năng đi qua cột')
ax.set_title('Phân tích nước đi mở màn tối ưu trong Connect 4 (Bàn 6x7)\nCột 3 trung tâm vượt trội hoàn toàn với 14 đường kết nối tiềm năng')
ax.set_xticks(cols)
ax.set_xticklabels([f"Cột {c}\n(Biên)" if c in [0,6] else f"Cột {c}" if c!=3 else "Cột 3\n(TRUNG TÂM)" for c in cols])
ax.set_ylim(0, 16.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
fig4_path = os.path.join(img_dir, 'fig_c4_first_move.png')
plt.savefig(fig4_path)
plt.close()
print(f"Saved {fig4_path}")

# ==============================================================================
# FIGURE 5: Dots and Boxes State Space Growth
# ==============================================================================
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

grid_names = ['2x2 dots\n(1 ô vuông)', '3x3 dots\n(4 ô vuông)', '4x4 dots\n(9 ô vuông)', '5x5 dots\n(16 ô vuông)']
num_lines = [4, 12, 24, 40]
state_space_log = [4 * np.log10(2), 12 * np.log10(2), 24 * np.log10(2), 40 * np.log10(2)]
game_tree_log = [np.log10(float(math.factorial(4))), np.log10(float(math.factorial(12))), np.log10(float(math.factorial(24))), float(np.sum([np.log10(i) for i in range(1, 41)]))]

x = np.arange(len(grid_names))
w = 0.35

ax.bar(x - w/2, state_space_log, w, label='Không gian trạng thái: log10(|S|)', color='#9b59b6')
ax.bar(x + w/2, game_tree_log, w, label='Cây trò chơi cực đại: log10(|Tree|)', color='#e67e22')

ax.set_ylabel('Độ lớn lũy thừa cơ số 10 (log10)')
ax.set_title('Bùng nổ tổ hợp trong trò chơi Dots and Boxes theo kích thước lưới')
ax.set_xticks(x)
ax.set_xticklabels(grid_names)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
fig5_path = os.path.join(img_dir, 'fig_dots_scaling.png')
plt.savefig(fig5_path)
plt.close()
print(f"Saved {fig5_path}")

print("All figures successfully created in", img_dir)
