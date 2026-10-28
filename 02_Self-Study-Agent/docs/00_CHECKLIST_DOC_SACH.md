# Checklist Lộ Trình Đọc Sách & Hoàn Thành "AlphaGo Simplified" Cấp Tốc

> **Mục tiêu**: Nắm vững toàn bộ tư duy kiến trúc của Deep Blue, AlphaGo và AlphaZero trong thời gian ngắn nhất (từ 7 đến 14 ngày), hiểu sâu bản chất thuật toán mà không bị kẹt vào việc huấn luyện mô hình tốn thời gian.

---

## 🚀 3 Bí Quyết "Đọc Nhanh - Hiểu Sâu - Tiết Kiệm Thời Gian"

1. **BÍ QUYẾT 1: Không tự huấn luyện lại từ đầu (Tận dụng `files/`)**
   - Huấn luyện Deep RL và MCTS có thể mất vài tiếng đến cả ngày trên máy tính cá nhân.
   - Tác giả **đã lưu sẵn toàn bộ trọng số mô hình (.h5) và bảng Q (.csv)** trong thư mục `files/`.
   - **Hành động**: Trong code, hãy comment dòng `model.fit()` hoặc vòng lặp train tự đấu, và thay bằng `model = keras.models.load_model('files/xxx.h5')`. Bạn sẽ có ngay một AI đỉnh cao để đấu thử và phân tích chỉ sau 2 giây!

2. **BÍ QUYẾT 2: Phương pháp "Trục 3 Trò Chơi" (Coin -> TicTacToe -> Connect Four)**
   - Cuốn sách có cấu trúc lặp lại tuyệt vời: Mỗi thuật toán mới luôn được thử nghiệm trên:
     1. **Coin Game** (Cực đơn giản, không gian trạng thái nhỏ) $\rightarrow$ *Đọc kỹ để hiểu bản chất toán học/thuật toán*.
     2. **Tic Tac Toe** (Không gian 3x3) $\rightarrow$ *Đọc kỹ để hiểu cách mở rộng lên mảng 2 chiều và mạng CNN*.
     3. **Connect Four** (Không gian lớn 6x7) $\rightarrow$ *Đọc lướt nhanh để xem cách tối ưu bộ nhớ/tốc độ (Vectorization)*.
   - Nếu bạn thiếu thời gian, chỉ cần đọc vững **Coin Game** và **Tic Tac Toe** là đã nắm được 90% tinh hoa của AlphaGo!

3. **BÍ QUYẾT 3: Sử dụng Simple Environment để tránh lỗi đồ họa GUI**
   - Trong thư mục `utils/`, tác giả cung cấp 2 loại môi trường:
     - Môi trường đồ họa với Turtle (`coin_env.py`, `ttt_env.py`, `conn_env.py`): Có giao diện trực quan nhưng chạy chậm và có thể lỗi trên máy chủ/terminal không màn hình.
     - Môi trường thuần text (`coin_simple_env.py`, `ttt_simple_env.py`, `conn_simple_env.py`): Chạy siêu tốc, lý tưởng khi chạy thử nghiệm hàng ngàn ván đấu.

---

## 📅 Lộ Trình Đề Xuất (7 Ngày Cấp Tốc)

| Ngày | Các Chương Cần Hoàn Thành | Trọng Tâm Kiến Thức |
| :--- | :--- | :--- |
| **Ngày 1** | Chương 1, 2, 3 | Khái niệm Rule-based AI, tìm kiếm nhìn trước (Look-ahead) |
| **Ngày 2** | Chương 4, 5, 6 | Đệ quy MiniMax, Cắt tỉa Alpha-Beta (Hiểu vì sao cắt giảm 97% thời gian) |
| **Ngày 3** | Chương 7, 8 | Hàm đánh giá thế cờ (Heuristics) và MCTS với công thức UCT |
| **Ngày 4** | Chương 9, 10, 11 | Deep Learning: Dùng CNN học bắt chước nước đi chuyên gia (Supervised Learning) |
| **Ngày 5** | Chương 12, 13 | Reinforcement Learning: Tabular Q-learning, Policy Gradients (REINFORCE) & Value Net |
| **Ngày 6** | Chương 14, 15, 16 | Vectorization tăng tốc Deep RL & Ghép nối hoàn chỉnh AlphaGo ban đầu |
| **Ngày 7** | Chương 17, 18, 19, 20, 21 | Tinh chỉnh siêu tham số, Đỉnh cao AlphaZero (Actor-Critic, tự học từ số 0) |

---

## ✅ Bảng Checklist Chi Tiết Từng Chương (Interactive Checklist)

### PHẦN I: AI DỰA TRÊN LUẬT (RULE-BASED AI)
*Mục tiêu: Hiểu cách tư duy giải bài toán trò chơi trước kỷ nguyên Deep Learning.*

- [x] **[Chương 1: Coin Game](file:///d:/AlphaGoSimplified/docs_vi/ch01_CoinGame.md)** `[Cốt lõi - 30 phút]`
  - [x] Hiểu luật chơi bốc xu (21 đồng, bốc 1 hoặc 2, bốc cuối cùng là thắng).
  - [x] Nắm vững thuật toán số dư `coins % 3` (thắng 100% khi đi sau).
  - [x] Chạy thử hàm `one_coin_game()` cho AI đấu với người chơi ngẫu nhiên.

- [x] **[Chương 2: Tic Tac Toe Look-Ahead](file:///d:/AlphaGoSimplified/docs_vi/ch02_TicTacToe.md)** `[Đọc nhanh - 20 phút]`
  - [x] Hiểu tư duy nhìn trước 1 bước (chọn ngay nước thắng).
  - [x] Hiểu tư duy nhìn trước 2 bước (chặn nước thắng của đối thủ).
  - [x] Hiểu tư duy nhìn trước 3 bước (tạo thế gọng kìm thắng kép).

- [ ] **[Chương 3: Connect Four 3 Steps](file:///d:/AlphaGoSimplified/docs_vi/ch03_ConnectFour.md)** `[Đọc lướt - 20 phút]`
  - [ ] Nắm vững khái niệm "nước đi tự sát" (thả quân khiến đối thủ thắng ngay ô phía trên).
  - [ ] Xem cách kết hợp hàm chặn và hàm tránh nước tự sát.

- [ ] **[Chương 4: Đệ Quy & MiniMax Tree Search](file:///d:/AlphaGoSimplified/docs_vi/ch04_MiniMax.md)** `[Cốt lõi - 45 phút]`
  - [ ] Hiểu cơ chế đệ quy gọi lại chính nó trong duyệt cây trò chơi.
  - [ ] Hiểu thuật toán Quy nạp ngược (*Backward Induction*) trong MiniMax.
  - [ ] Nắm vững cách tính giá trị tối đa (*maximized payoff*) của Coin Game.

- [ ] **[Chương 5: Depth Pruning trong MiniMax](file:///d:/AlphaGoSimplified/docs_vi/ch05_DepthPruning.md)** `[Đọc nhanh - 30 phút]`
  - [ ] Hiểu lý do vì sao MiniMax duyệt hết cây bị bùng nổ tổ hợp trong Connect Four ($7^{42}$ trạng thái).
  - [ ] Nắm cách đặt tham số `depth` để dừng tìm kiếm sớm.

- [ ] **[Chương 6: Cắt Tỉa Alpha-Beta](file:///d:/AlphaGoSimplified/docs_vi/ch06_AlphaBetaPruning.md)** `[Cốt lõi - 45 phút]`
  - [ ] Hiểu định nghĩa toán học của $\alpha$ (giá trị tốt nhất người chơi tối đa đảm bảo được) và $\beta$ (giá trị người chơi tối thiểu đảm bảo).
  - [ ] Nắm điều kiện cắt nhánh: khi $\alpha \ge \beta$.
  - [ ] Kiểm chứng kết quả thực nghiệm: Thời gian suy nghĩ giảm 97% so với MiniMax thuần!

- [ ] **[Chương 7: Hàm Đánh Giá Thế Cờ](file:///d:/AlphaGoSimplified/docs_vi/ch07_PositionEvaluation.md)** `[Đọc nhanh - 30 phút]`
  - [ ] Hiểu vai trò của hàm Heuristic khi duyệt cây chạm độ sâu 0 mà ván cờ chưa kết thúc.
  - [ ] Xem cách gán điểm cho chuỗi 2 quân, 3 quân tiềm năng trong Connect Four.

- [ ] **[Chương 8: Monte Carlo Tree Search (MCTS)](file:///d:/AlphaGoSimplified/docs_vi/ch08_MonteCarloTreeSearch.md)** `[Cực kỳ quan trọng - 60 phút]`
  - [ ] Hiểu tại sao cờ vây không dùng được hàm đánh giá như cờ vua mà phải dùng MCTS.
  - [ ] Nắm vững 4 giai đoạn của MCTS:
    1. **Selection (Lựa chọn)** theo công thức UCT.
    2. **Expansion (Mở rộng)** thêm node mới.
    3. **Simulation / Rollout (Mô phỏng ngẫu nhiên)** đến hết ván.
    4. **Backpropagation (Lan truyền ngược)** cập nhật số lần thăm $N$ và số trận thắng $W$.
  - [ ] Nắm công thức UCT: $\frac{w_i}{n_i} + c \sqrt{\frac{\ln N_i}{n_i}}$ (cân bằng giữa Khai thác Exploitation và Khám phá Exploration).

---

### PHẦN II: HỌC SÂU (DEEP LEARNING)
*Mục tiêu: Dùng mạng nơ-ron để thay thế các hàm luật và heuristics thủ công.*

- [ ] **[Chương 9: Deep Learning trong Coin Game](file:///d:/AlphaGoSimplified/docs_vi/ch09_DeepLearningCoinGame.md)** `[Cốt lõi - 40 phút]`
  - [ ] Nắm cách dùng Keras/TensorFlow xây dựng mạng nơ-ron phân loại nước đi (Policy Network).
  - [ ] Phân biệt **Fast Policy Network** (mạng nhỏ, suy luận cực nhanh dùng cho mô phỏng) và **Strong Policy Network** (mạng sâu hơn, dự đoán chuẩn xác hơn).

- [ ] **[Chương 10: Policy Network với CNN trong Tic Tac Toe](file:///d:/AlphaGoSimplified/docs_vi/ch10_PolicyNetworksTicTacToe.md)** `[Cốt lõi - 45 phút]`
  - [ ] Hiểu tại sao dùng lớp tích chập Conv2D cho bàn cờ (bảo toàn tính chất không gian lân cận).
  - [ ] Nắm quy trình sinh dữ liệu chuyên gia từ thuật toán MiniMax Alpha-Beta (Chương 6) để dạy cho CNN.

- [ ] **[Chương 11: Policy Network trong Connect Four](file:///d:/AlphaGoSimplified/docs_vi/ch11_PolicyNetworkConnectFour.md)** `[Đọc lướt - 30 phút]`
  - [ ] Xem cách tự sinh dữ liệu từ trận đấu giữa MCTS và MiniMax để huấn luyện mạng nơ-ron cho Connect Four.

---

### PHẦN III: HỌC TĂNG CƯỜNG (REINFORCEMENT LEARNING)
*Mục tiêu: Để AI tự chơi và tự cải thiện mà không cần dữ liệu chuyên gia của con người.*

- [ ] **[Chương 12: Tabular Q-Learning trong Coin Game](file:///d:/AlphaGoSimplified/docs_vi/ch12_TabularQLearning.md)** `[Cốt lõi - 45 phút]`
  - [ ] Hiểu các thành phần của RL: Trạng thái ($S$), Hành động ($A$), Phần thưởng ($R$).
  - [ ] Nắm phương trình Bellman: $Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$.
  - [ ] Xem file `files/coin_Qs.csv` để thấy bảng giá trị Q hội tụ về chiến thuật hoàn hảo.

- [ ] **[Chương 13: Policy Gradients & Value Network](file:///d:/AlphaGoSimplified/docs_vi/ch13_DeepReinforcementLearningCoin.md)** `[Cực kỳ quan trọng - 60 phút]`
  - [ ] Nắm thuật toán Policy Gradient (REINFORCE): Tăng xác suất các nước đi dẫn đến chiến thắng cuối cùng, giảm xác suất nước đi thua cuộc.
  - [ ] Hiểu phần thưởng chiết khấu (*Discounted Reward*) $\gamma^t R$.
  - [ ] Hiểu vai trò của **Value Network** (Mạng giá trị): Dự đoán xác suất thắng từ trạng thái hiện tại (không cần mô phỏng đến hết ván!).

- [ ] **[Chương 14: Vectorization & Xử lý Nước đi Sai Luật](file:///d:/AlphaGoSimplified/docs_vi/ch14_VectorizationTicTacToe.md)** `[Cốt lõi - 45 phút]`
  - [ ] Xử lý nước đi không hợp lệ (Illegal moves) bằng hình phạt phần thưởng âm (Negative reward).
  - [ ] Kỹ thuật mã hóa đối xứng độc lập người chơi: Quân của mình luôn là $+1$, đối thủ là $-1$. Nhờ đó 1 mạng duy nhất dùng được cho cả 2 bên!
  - [ ] Kỹ thuật Vectorization để chạy song song hàng trăm ván cờ trên GPU.

- [ ] **[Chương 15: Value Network trong Connect Four](file:///d:/AlphaGoSimplified/docs_vi/ch15_ValueNetworkConnectFour.md)** `[Đọc lướt - 30 phút]`
  - [ ] Áp dụng Policy Gradient và Value Network lên bàn cờ 6x7 của Connect Four.

---

### PHẦN IV: THUẬT TOÁN ALPHAGO & ALPHAZERO
*Mục tiêu: Hợp nhất toàn bộ các mảnh ghép lại thành cỗ máy AI bất khả chiến bại.*

- [ ] **[Chương 16: Cài Đặt AlphaGo Hoàn Chỉnh](file:///d:/AlphaGoSimplified/docs_vi/ch16_AlphaGoCoinGame.md)** `[Đỉnh cao - 60 phút]`
  - [ ] Nắm vững bức tranh kiến trúc tổng thể AlphaGo:
    - **MCTS** làm khung sườn tìm kiếm cây.
    - **Strong Policy Network** hướng dẫn chọn các nhánh con hứa hẹn nhất.
    - **Fast Policy Network** thực hiện rollout nhanh chóng.
    - **Value Network** đánh giá thế cờ tại node lá để kết hợp cùng kết quả rollout.
  - [ ] Thấy được AI đạt tỷ lệ thắng 100% trước đối thủ dựa trên luật.

- [ ] **[Chương 17: AlphaGo Đa Năng (TicTacToe & Connect Four)](file:///d:/AlphaGoSimplified/docs_vi/ch17_AlphaGoTicTacToe.md)** `[Cốt lõi - 45 phút]`
  - [ ] Xem cách thiết kế code trừu tượng (Generalizable code) dùng chung một class `AlphaGo` cho cả 2 trò chơi.
  - [ ] Kiểm chứng AlphaGo hòa tuyệt đối với AI MiniMax hoàn hảo trong Tic Tac Toe (đã giải quyết bài toán).

- [ ] **[Chương 18: Tinh Chỉnh Siêu Tham Số AlphaGo](file:///d:/AlphaGoSimplified/docs_vi/ch18_AlphaGoTuning.md)** `[Đọc nhanh - 30 phút]`
  - [ ] Hiểu cách dùng Grid Search để tinh chỉnh: số lần mô phỏng rollout, trọng số kết hợp giữa Value Network và Rollout, hằng số khám phá $c$.

- [ ] **[Chương 19: Actor-Critic & AlphaZero](file:///d:/AlphaGoSimplified/docs_vi/ch19_ActorCriticAlphaZero.md)** `[Đỉnh cao - 60 phút]`
  - [ ] Hiểu sự khác biệt mang tính cách mạng giữa AlphaGo và AlphaZero:
    - Không cần dữ liệu của con người (Tabula Rasa).
    - Gom 2 mạng tách rời thành **1 mạng nơ-ron duy nhất có 2 đầu ra**: Đầu Actor (Policy) và Đầu Critic (Value).
    - Loại bỏ hoàn toàn giai đoạn rollout ngẫu nhiên chậm chạp, chỉ dùng Value Head để đánh giá node lá!
  - [ ] Chứng minh AlphaZero đánh bại AlphaGo cũ trong Coin Game.

- [ ] **[Chương 20: Tự Đấu Lặp (Iterative Self-Play) trong Tic Tac Toe](file:///d:/AlphaGoSimplified/docs_vi/ch20_AlphaZeroTicTacToe.md)** `[Cốt lõi - 45 phút]`
  - [ ] Giải quyết bài toán "Mục tiêu di động" (Moving target): Cho AI hiện tại đấu với bản sao đóng băng (Checkpoint) của chính nó ở các thế hệ trước.
  - [ ] Khi tỷ lệ thắng vượt ngưỡng quy định, cập nhật mô hình đóng băng lên phiên bản mới nhất.

- [ ] **[Chương 21: AlphaZero Trong Trò Chơi Chưa Có Lời Giải](file:///d:/AlphaGoSimplified/docs_vi/ch21_AlphaZeroUnsolvedGames.md)** `[Tổng kết - 45 phút]`
  - [ ] Áp dụng AlphaZero cho Connect Four (không cần benchmark với lời giải toán học).
  - [ ] Tự cải tiến qua nhiều vòng lặp và đánh bại AlphaGo của Chương 18.

---

## 🎯 Checklist Thực Hành Code Tối Thiểu Để "Tốt Nghiệp" Khóa Học
Nếu bạn chỉ có vài giờ để code thực chiến, hãy chạy thử đúng 4 notebook sau:
1. [ ] Mở [ch04MiniMax.ipynb](file:///d:/AlphaGoSimplified/ch04MiniMax.ipynb) $\rightarrow$ Xem thuật toán đệ quy MiniMax chạy.
2. [ ] Mở [ch08MonteCarloTreeSearch.ipynb](file:///d:/AlphaGoSimplified/ch08MonteCarloTreeSearch.ipynb) $\rightarrow$ Xem MCTS xây dựng cây tìm kiếm qua rollout.
3. [ ] Mở [ch16AlphaGoCoinGame.ipynb](file:///d:/AlphaGoSimplified/ch16AlphaGoCoinGame.ipynb) $\rightarrow$ Xem cách nạp 3 file model `.h5` và kết hợp với MCTS.
4. [ ] Mở [ch20AlphaZeroTicTacToe.ipynb](file:///d:/AlphaGoSimplified/ch20AlphaZeroTicTacToe.ipynb) $\rightarrow$ Xem kiến trúc mạng 2 đầu Actor-Critic của AlphaZero.
