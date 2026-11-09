# Adversarial Search and Games

## Defining a Game
* [Defining Tic-Tac-Toe](tictactoe_definitions.ipynb)

## Connection to search with nondeterministic actions
* [Solving Tic-Tac-Toe with And-Or-Tree Search](tictactoe_and_or_tree_search.ipynb). Here the opponent is seen as part of the environment, i.e.,
each action by the player is followed by an unknown action of the opponent which, from the viewpoint of the player makes the outcomes of actions nondeterministic.
* Here are the basic functions for 
[Tic-Tac-Toe](tictactoe_definitions.ipynb).

## Search in Unknown Environments
* Experimental environment: [Micromouse](https://en.wikipedia.org/wiki/Micromouse) is an event where small robotic mice compete to solve a maze. 
You can watch the video [The Fastest Maze-Solving Competition On Earth](https://www.youtube.com/watch?v=ZMQbHMgK2rw).
You can test your own agent function using the 
  [Micromouse Simulator](https://github.com/mackorone/mms-python). 

## Solving Games Using Adversarial Search
* [Solving Tic-Tac-Toe with Minimax Search and Alpha-Beta Pruning](tictactoe_alpha_beta_tree_search.ipynb)
* [Solving Tic-Tac-Toe with Heuristic Alpha-Beta Tree Search](tictactoe_heuristic_alpha_beta_tree_search.ipynb)
* [Solving Tic-Tac-Toe with Pure Monte Carlo Search](tictactoe_pure_monte_carlo_search.ipynb)
* [Solving Tic-Tac-Toe with Pure Monte Carlo Search + UCB1 Selection Policy](tictactoe_monte_carlo_tree_search_restricted.ipynb)

## Interactive Game Play
* [Play Tic-Tac-Toe Interactively (Simple Implementation)](tictactoe_interactive.ipynb)

## Exercises
* [Adversarial Search: Playing Connect 4](assignment_connect4.ipynb)
* [Adversarial Search: Playing "Mean" Connect 4](assignment_mean_connect4.ipynb)
* [Adversarial Search: Playing Dots and Boxes](assignment_dots_and_boxes.ipynb)

---

## Hướng dẫn cài đặt và chạy thực nghiệm Lab 05

### 1. Yêu cầu thư viện Python
Cài đặt Python $\ge 3.10$ cùng các thư viện khoa học dữ liệu cơ bản:
```bash
pip install numpy pandas matplotlib ipython jupyter
```

### 2. Cấu trúc tập tin hoàn chỉnh
* **7 notebook Tic-Tac-Toe** (đã điền bổ sung kiểm thử chuẩn `seed=42`, bảng tổng hợp và nhận xét):
  * `tictactoe_definitions.ipynb` (Mô hình trò chơi & 1.000 ván Random vs Random)
  * `tictactoe_and_or_tree_search.ipynb` (AND-OR Tree Search & kế hoạch điều kiện)
  * `tictactoe_alpha_beta_tree_search.ipynb` (Minimax, Alpha-Beta & Move Ordering)
  * `tictactoe_heuristic_alpha_beta_tree_search.ipynb` (Heuristic Cutoff = 2, 4)
  * `tictactoe_pure_monte_carlo_search.ipynb` (PMCS $N=10, 100, 1000$)
  * `tictactoe_monte_carlo_tree_search_restricted.ipynb` (MCTS `UCT_depth1` với UCB1)
  * `tictactoe_interactive.ipynb` (Chơi tương tác & ghi vết đối kháng `ab_player`)
* **3 bài tập mở rộng**:
  * `assignment_connect4.ipynb` (Connect 4: $6\times 7$, Scalability, Profiling, Heuristic, PMCS, Best First Move)
  * `assignment_mean_connect4.ipynb` ("Mean" Connect 4: Luật cướp quân đáy, phát hiện chu trình 3 lần, Steal-Aware Heuristic, PMCS)
  * `assignment_dots_and_boxes.ipynb` (Dots and Boxes: Extra Turn Rule, Alpha-Beta chính xác $3\times 3$, Chain-Aware Heuristic $4\times 4$ & $5\times 5$, PMCS, Best First Move)
* **Tiện ích bổ trợ (`../scripts/`)**:
  * `../scripts/nb_executor.py`: Công cụ thực thi trực tiếp toàn bộ mã nguồn các `.ipynb` và lưu kết quả/biểu đồ vào trong từng notebook.
  * `../scripts/generate_figures.py`: Tạo lại 5 biểu đồ báo cáo độ phân giải cao trong thư mục `../img/`.

### 3. Cách chạy
1. **Chạy tương tác bằng Jupyter:**
   Mở terminal trong thư mục `lab05 - game/` và chạy:
   ```bash
   jupyter notebook
   ```
   Sau đó chọn **Run All** cho từng notebook (lưu ý ở `tictactoe_interactive.ipynb`, các ô gọi `input()` cần nhập tay từ người dùng; riêng ô mô phỏng tự động cuối file chạy không cần nhập tay).
2. **Chạy lại tự động toàn bộ notebook (không cần mở giao diện Jupyter):**
   Từ thư mục `01_Group-Labs/lab5 - game/`:
   ```bash
   python scripts/nb_executor.py
   python scripts/generate_figures.py
   ```
3. **Biên dịch báo cáo LaTeX (`../main.tex`):**
   Biên dịch 2 lượt với `pdflatex` từ thư mục `01_Group-Labs/lab5 - game/` để cập nhật mục lục và danh mục hình/bảng:
   ```bash
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```
