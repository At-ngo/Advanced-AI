# Chương 5: Cắt Tỉa Theo Độ Sâu (Depth Pruning) Trong MiniMax
*Nguyên tác: Chapter 5: Depth Pruning in MiniMax*
*Notebook gốc:* [ch05DepthPruning.ipynb](file:///d:/AlphaGoSimplified/ch05DepthPruning.ipynb)

---

## 1. Vấn Đề Bùng Nổ Tổ Hợp (Combinatorial Explosion)

Trong Tic Tac Toe, cây trò chơi có tối đa $9! = 362,880$ lá. Máy tính hiện đại duyệt hết cây chỉ mất vài giây. MiniMax duyệt trọn vẹn sẽ tìm ra lời giải hoàn hảo (luôn hòa hoặc thắng).

Tuy nhiên, trong **Connect Four**:
- Bàn cờ 6x7 có tối đa 42 lượt đi.
- Mỗi lượt có trung bình 7 lựa chọn.
- Số nhánh lá lên đến $7^{42} \approx 3 \times 10^{35}$!
- Dù dùng siêu máy tính mạnh nhất hành tinh cũng phải mất hàng tỷ năm mới duyệt hết.

**Giải pháp**: Cắt tỉa theo độ sâu (**Depth Pruning**). Ta chỉ cho phép thuật toán nhìn trước một số bước nhất định (ví dụ $d = 3$ hoặc $d = 4$), sau đó dừng lại và ước lượng kết quả.

---

## 2. Cài Đặt MiniMax Kèm Cắt Tỉa Độ Sâu

Khi đệ quy, ta giảm biến `depth` đi 1 đơn vị sau mỗi lượt. Nếu `depth == 0` mà ván cờ chưa kết thúc, tạm thời coi đó là một ván hòa (`payoff = 0`):

```python
def max_payoff(env, reward, done, depth):
    # 1. Trò chơi kết thúc
    if done:
        return -1 if reward != 0 else 0
        
    # 2. Chạm đáy tìm kiếm (Depth Pruning)
    if depth == 0:
        return 0  # Giả định tạm thời là hòa
        
    best_payoff = -2
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, reward, done, _ = env_copy.step(m)
        
        # Giảm depth đi 1 ở tầng kế tiếp
        opponent_payoff = max_payoff(env_copy, reward, done, depth - 1)
        my_payoff = -opponent_payoff
        
        if my_payoff > best_payoff:
            best_payoff = my_payoff
            
    return best_payoff
```

```python
def MiniMax_depth(env, depth=3):
    wins, ties, losses = [], [], []
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, reward, done, _ = env_copy.step(m)
        if done and reward != 0:
            return m
            
        opponent_payoff = max_payoff(env_copy, reward, done, depth - 1)
        my_payoff = -opponent_payoff
        
        if my_payoff == 1:
            wins.append(m)
        elif my_payoff == 0:
            ties.append(m)
        else:
            losses.append(m)
            
    if wins: return choice(wins)
    if ties: return choice(ties)
    return env.sample()
```

---

## 3. Hiệu Quả & Điểm Yếu Cần Giải Quyết

### Hiệu quả:
- Thời gian ra quyết định trong Connect Four giảm từ "vô tận" xuống chỉ còn **khoảng 0.1 giây / nước đi** với `depth = 3`.
- AI với `depth = 3` dễ dàng đánh bại đối thủ chơi ngẫu nhiên và đối thủ nhìn trước 1-2 bước.

### Điểm yếu:
1. **Thiếu chính xác**: Khi dừng ở độ sâu 0, việc gán điểm hòa (`0`) là quá thô sơ (vì một bên có thể đang nắm giữ thế cờ áp đảo 3 quân liên tiếp). Vấn đề này sẽ được giải quyết bằng **Hàm đánh giá thế cờ (Position Evaluation)** ở Chương 7.
2. **Vẫn còn duyệt thừa**: MiniMax vẫn duyệt qua cả những nhánh hoàn toàn vô nghĩa. Ta có thể tăng tốc thêm gấp hàng chục lần nhờ **Cắt tỉa Alpha-Beta** ở Chương 6!
