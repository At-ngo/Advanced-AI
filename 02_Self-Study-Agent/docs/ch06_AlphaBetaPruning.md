# Chương 6: Cắt Tỉa Alpha-Beta (Alpha-Beta Pruning)
*Nguyên tác: Chapter 6: Alpha-Beta Pruning*
*Notebook gốc:* [ch06AlphaBetaPruning.ipynb](file:///d:/AlphaGoSimplified/ch06AlphaBetaPruning.ipynb)

---

## 1. Bản Chất Toán Học Của Cắt Tỉa Alpha-Beta

Khi đang duyệt cây trò chơi:
- Giả sử bạn đã tìm thấy một nước đi đảm bảo mang lại cho bạn điểm số ít nhất là **$\alpha = 0$ (Hòa)**.
- Khi kiểm tra một nhánh nước đi khác, đối thủ có một phương án phản công khiến điểm số của bạn chỉ còn **$-1$ (Thua)**.
- Vậy bạn có cần tiếp tục tính toán các phản công khác của đối thủ ở nhánh đó không? **Hoàn toàn không!** Vì đối thủ đã có thể ép bạn thua ở nhánh này, bạn chắc chắn sẽ chọn nước đi đầu tiên đã đảm bảo hòa. Nhánh thứ hai có thể bị bỏ qua ngay lập tức!

### Định nghĩa $\alpha$ và $\beta$:
- **$\alpha$**: Điểm số tối thiểu tốt nhất mà người chơi hiện tại (Maximizer) đã chắc chắn đạt được cho đến nay.
- **$\beta$**: Điểm số tối đa tốt nhất mà đối thủ (Minimizer) cho phép bạn đạt được.
- **Điều kiện cắt nhánh (Pruning Condition)**: Bất cứ khi nào $\alpha \ge \beta$ (hoặc trong dạng đối xứng Negamax: $\alpha \ge -\beta$), ta lập tức dừng duyệt vòng lặp (`break`) và bỏ qua toàn bộ cây con bên dưới!

---

## 2. Cài Đặt Mã Nguồn Trong Tic Tac Toe & Connect Four

### 2.1. Cắt tỉa Alpha-Beta trong Tic Tac Toe
```python
def maximized_payoff_ttt(env, reward, done, alpha, beta):
    if done:
        return -1 if reward != 0 else 0
        
    if alpha is None: alpha = -2
    if beta is None: beta = -2
    
    best_payoff = alpha if env.turn == "X" else beta
    
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, reward, done, _ = env_copy.step(m)
        
        # Đệ quy truyền ngược alpha, beta
        opponent_payoff = maximized_payoff_ttt(env_copy, reward, done, alpha, beta)
        my_payoff = -opponent_payoff
        
        if my_payoff > best_payoff:
            best_payoff = my_payoff
            if env.turn == "X":
                alpha = best_payoff
            if env.turn == "O":
                beta = best_payoff
                
        # Cắt nhánh thần tốc: Bỏ qua toàn bộ cây con còn lại!
        if alpha >= -beta:
            break
            
    return best_payoff
```

### 2.2. Kết hợp với Depth Pruning trong Connect Four
```python
def max_payoff_conn(env, reward, done, depth, alpha, beta):
    if done:
        return -1 if reward != 0 else 0
    if depth == 0:
        return 0
        
    best_payoff = -2
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, reward, done, _ = env_copy.step(m)
        
        opponent_payoff = max_payoff_conn(env_copy, reward, done, depth - 1, alpha, beta)
        my_payoff = -opponent_payoff
        
        if my_payoff > best_payoff:
            best_payoff = my_payoff
            alpha = max(alpha, best_payoff)
            
        if alpha >= beta:
            break  # Cắt tỉa
            
    return best_payoff
```

---

## 3. Kết Quả Thực Nghiệm Chấn Động

Trong thực nghiệm của tác giả trong notebook:
- **Thời gian suy nghĩ**: MiniMax thông thường mất trung bình **~4.8 giây** cho một nước đi mở đầu trong Tic Tac Toe.
- **Sau khi thêm Alpha-Beta Pruning**: Thời gian giảm xuống chỉ còn **~0.15 giây**!
- **Tốc độ cải thiện**: Giảm tới **97% thời gian tính toán** mà **kết quả nước đi đưa ra là hoàn toàn giống hệt 100%**!
- Trong Connect Four, Alpha-Beta cho phép nâng độ sâu tìm kiếm từ `depth = 3` lên `depth = 5` hoặc `6` trong cùng một khoảng thời gian chờ đợi.
