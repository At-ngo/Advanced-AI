# Chương 4: Đệ Quy và Tìm Kiếm Cây MiniMax (MiniMax Tree Search)
*Nguyên tác: Chapter 4: Recursion and MiniMax Tree Search*
*Notebook gốc:* [ch04MiniMax.ipynb](file:///d:/AlphaGoSimplified/ch04MiniMax.ipynb)

---

## 1. Bản Chất Của MiniMax và Quy Nạp Ngược (Backward Induction)

Trong lý thuyết trò chơi đối kháng có tổng bằng 0 (*Zero-Sum Game*), lợi ích của người này là thiệt hại của người kia:
$$\text{Lợi ích của tôi} = - (\text{Lợi ích của đối thủ})$$

Nếu mỗi người chơi đều hành động duy lý để tối đa hóa phần thưởng của mình:
- Ở lượt của **tôi**, tôi muốn chọn nước đi có phần thưởng **lớn nhất (Max)**.
- Ở lượt của **đối thủ**, đối thủ sẽ chọn nước đi khiến phần thưởng của tôi **nhỏ nhất (Min)** (tương đương với việc đối thủ tối đa hóa phần thưởng của họ).

### Thuật toán Negamax (Dạng rút gọn của MiniMax)
Thay vì viết 2 hàm `maximize` và `minimize` riêng biệt, ta áp dụng công thức đảo dấu:
$$\text{My Payoff} = - \text{Opponent's Max Payoff}$$
Nhờ đó chỉ cần **duy nhất một hàm đệ quy**!

---

## 2. Cài Đặt MiniMax Cho Coin Game

### 2.1. Hàm đệ quy tính lợi ích tối đa (`maximized_payoff`)
```python
from copy import deepcopy
from random import choice

def maximized_payoff(env, reward, done):
    # Điều kiện dừng: Ván cờ đã kết thúc sau lượt đi trước
    if done:
        return -1  # Đối thủ vừa đi xong và thắng -> ta thua (-1)
        
    best_payoff = -2  # Khởi tạo giá trị nhỏ nhất
    
    # Duyệt qua tất cả các nước đi khả dĩ
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, reward, done, _ = env_copy.step(m)
        
        # Đệ quy: Hỏi xem đối thủ sẽ đạt được lợi ích tối đa là bao nhiêu
        opponent_payoff = maximized_payoff(env_copy, reward, done)
        
        # Lợi ích của ta là số đối của đối thủ
        my_payoff = -opponent_payoff
        
        if my_payoff > best_payoff:
            best_payoff = my_payoff
            
    return best_payoff
```

### 2.2. Hàm chọn nước đi MiniMax
```python
def MiniMax(env):
    wins = []
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, reward, done, _ = env_copy.step(m)
        if done and reward == 1:
            return m  # Thắng ngay
            
        opponent_payoff = maximized_payoff(env_copy, reward, done)
        my_payoff = -opponent_payoff
        if my_payoff == 1:
            wins.append(m)
            
    if wins:
        return choice(wins)
    return env.sample()
```

---

## 3. Đánh Giá & Ý Nghĩa
- Thuật toán MiniMax đệ quy duyệt toàn bộ cây trò chơi cho đến trạng thái kết thúc (*Terminal State*).
- Trong Coin Game (chỉ có 21 xu), số lượng trạng thái rất nhỏ nên MiniMax giải quyết triệt để trò chơi trong chớp mắt.
- **Kết quả**: MiniMax thi đấu với `rule_based_AI` (từ Chương 1) đạt tỷ lệ hòa và thắng tương đương nhau, chứng minh MiniMax hoàn toàn tìm ra được chiến lược toán học tối ưu mà không cần bất kỳ luật cứng nào do con người nạp vào!
