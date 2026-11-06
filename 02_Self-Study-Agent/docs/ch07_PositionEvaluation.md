# Chương 7: Hàm Đánh Giá Thế Cờ (Position Evaluation Function)
*Nguyên tác: Chapter 7: Position Evaluation in MiniMax*
*Notebook gốc:* [ch07PositionEvaluationFunction.ipynb](file:///d:/AlphaGoSimplified/ch07PositionEvaluationFunction.ipynb)

---

## 1. Bí Quyết Của Deep Blue (1997)

Khi Deep Blue đánh bại Garry Kasparov vào năm 1997, cờ vua có không gian trạng thái $10^{120}$ — không một siêu máy tính nào có thể duyệt tới tận cuối ván. Deep Blue duyệt cây khoảng 6 đến 12 bước (kết hợp cắt tỉa Alpha-Beta), và khi chạm độ sâu tối đa, nó sử dụng **Hàm đánh giá thế cờ (Position Evaluation Function)**.

Hàm đánh giá nhận đầu vào là trạng thái bàn cờ hiện tại và trả về một điểm số heuristic đại diện cho ưu thế:
$$\text{Score} \in [-1, 1]$$
- Điểm dương lớn ($+1$): Bên ta có ưu thế áp đảo / gần như thắng chắc.
- Điểm âm lớn ($-1$): Đối thủ có ưu thế áp đảo.
- Điểm xấp xỉ 0: Thế cờ cân bằng.

Thay vì coi mọi trạng thái chưa xong là hòa (`0`) như ở Chương 5, hàm đánh giá giúp AI biết hướng đi nào mang lại thế cờ đẹp hơn nhiều lần!

---

## 2. Thiết Kế Hàm Đánh Giá Cho Connect Four

Trong Connect Four, thế cờ mạnh là khi một người chơi sở hữu nhiều chuỗi quân tiềm năng chưa bị chặn:
- **Chuỗi 3 quân liên tiếp** và còn ô trống ở hai đầu: Đe dọa thắng ngay ở lượt sau (trọng số rất cao: ví dụ $+0.5$).
- **Chuỗi 2 quân liên tiếp**: Tiềm năng phát triển thành chuỗi 3 hoặc 4 (trọng số nhỏ hơn: ví dụ $+0.1$).
- **Chiếm cột trung tâm (Cột 3)**: Đem lại khả năng tạo đường chéo và ngang phong phú nhất.

Tác giả sử dụng một mô hình hồi quy / phân loại thống kê dựa trên các đặc trưng này để dự đoán xác suất thắng.

---

## 3. Tích Hợp Vào MiniMax

Khi đệ quy chạm `depth == 0`:
```python
def eval_payoff_conn(env, depth, alpha, beta, eval_func):
    if env.done:
        return -1 if env.reward != 0 else 0
        
    # Thay vì return 0 khi chạm đáy, ta gọi hàm đánh giá thế cờ!
    if depth == 0:
        return eval_func(env)
        
    best_payoff = -2
    for m in env.validinputs:
        env_copy = deepcopy(env)
        env_copy.step(m)
        opponent_payoff = eval_payoff_conn(env_copy, depth - 1, alpha, beta, eval_func)
        my_payoff = -opponent_payoff
        if my_payoff > best_payoff:
            best_payoff = my_payoff
        alpha = max(alpha, best_payoff)
        if alpha >= beta:
            break
    return best_payoff
```

---

## 4. Kết Quả & Giới Hạn Dẫn Đến MCTS
- AI có hàm đánh giá thế cờ đánh bại hoàn toàn AI MiniMax depth 3 không có hàm đánh giá với tỷ lệ thắng **>80%**.
- **Tuy nhiên**: Trong cờ vây (Go), việc viết một hàm đánh giá thế cờ heuristic bằng tay là điều bất khả thi vì thế cờ quá trừu tượng, trực giác và phụ thuộc vào toàn cục bàn cờ 19x19. Đó là lý do nhân loại đã phát minh ra **Monte Carlo Tree Search (MCTS)** ở Chương 8!
