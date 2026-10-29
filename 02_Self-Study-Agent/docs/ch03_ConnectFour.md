# Chương 3: Nhìn Trước 3 Bước Trong Connect Four
*Nguyên tác: Chapter 3: Planning Three Steps Ahead in Connect Four*
*Notebook gốc:* [ch03ConnectFour.ipynb](file:///d:/AlphaGoSimplified/ch03ConnectFour.ipynb)

---

## 1. Giới Thiệu Trò Chơi Connect Four (Cờ Thả 4 Nối)

Connect Four là trò chơi phổ biến với bàn cờ thẳng đứng gồm **6 hàng x 7 cột** (tổng cộng 42 ô):
- Hai người chơi lần lượt thả các đĩa màu (Đỏ hoặc Vàng) vào một trong 7 cột (từ 0 đến 6).
- Đĩa rơi xuống ô trống thấp nhất của cột đó do trọng lực.
- Người đầu tiên tạo được đường thẳng gồm **4 đĩa cùng màu liên tiếp** (ngang, dọc, hoặc chéo) sẽ thắng cuộc.
- Nếu đầy 42 ô mà không ai tạo được chuỗi 4, kết quả là hòa.

Không gian trạng thái của Connect Four là khoảng $4.5 \times 10^{12}$ trạng thái — lớn hơn rất nhiều so với Coin Game ($22$) hay Tic Tac Toe ($5,478$).

---

## 2. Thách Thức Khi Nhìn Trước Trong Connect Four

Khác với Tic Tac Toe, khi thả quân vào Connect Four ta phải đối mặt với **Nước Đi Tự Sát (Suicidal Moves)**:
- Nếu ta thả đĩa vào cột $C$, đĩa của ta sẽ nằm ở hàng $R$.
- Khi đó, ô ngay phía trên $(R+1, C)$ trở thành ô trống thấp nhất kế tiếp.
- Nếu ô $(R+1, C)$ chính là ô giúp đối thủ nối thành 4 đĩa $\rightarrow$ Nước đi của ta đã "dâng chiến thắng" cho đối thủ!

### Chiến lược 3 bước hoàn chỉnh:
1. **Bước 1**: Kiểm tra nếu có cột nào thả vào là thắng ngay $\rightarrow$ Thả ngay lập tức.
2. **Bước 2**:
   - Xác định các cột đối thủ có thể thắng ở lượt sau $\rightarrow$ **Cần chặn (Moves to block)**.
   - Xác định các cột nếu ta thả vào sẽ giúp đối thủ thắng ngay ô phía trên $\rightarrow$ **Cần tránh (Moves to avoid)**.
3. **Bước 3**: Mô phỏng 3 lượt để tìm cột có xác suất mở đường chiến thắng cao nhất trong tương lai.

---

## 3. Cài Đặt Thuật Toán Python

### 3.1. Phân loại nước chặn và nước cần tránh
```python
def conn_think2(env):
    # Ưu tiên 1: Thắng ngay lập tức
    for m in env.validinputs:
        env_copy = deepcopy(env)
        _, r, done, _ = env_copy.step(m)
        if done and r != 0:
            return m
            
    # Ưu tiên 2: Tìm nước chặn và nước tránh
    avoid = []
    block = []
    for m1 in env.validinputs:
        env_copy = deepcopy(env)
        env_copy.step(m1)
        for m2 in env_copy.validinputs:
            env_copy2 = deepcopy(env_copy)
            _, r, done, _ = env_copy2.step(m2)
            if done and r != 0:
                if m1 == m2:
                    # Nếu đối thủ thắng tại chính cột này -> nước tự sát!
                    avoid.append(m1)
                else:
                    # Đối thủ thắng ở cột khác -> cần chặn cột đó
                    block.append(m2)
                    
    # Lựa chọn nước đi an toàn
    safe_moves = [m for m in env.validinputs if m not in avoid]
    for b in block:
        if b in safe_moves:
            return b  # Chặn đối thủ một cách an toàn
            
    if safe_moves:
        return choice(safe_moves)
    return env.sample()
```

---

## 4. Kết Luận & Hạn Chế
- Thuật toán nhìn trước 3 bước giúp AI đạt tỷ lệ thắng **>90%** trước đối thủ ngẫu nhiên.
- Tuy nhiên, việc hardcode các luật kiểm tra ngày càng trở nên bất khả thi khi mở rộng lên 4, 5 hay 6 bước trong bàn cờ 42 ô.
- Chương tiếp theo sẽ giới thiệu giải pháp tổng quát cho mọi trò chơi đối kháng: **Thuật toán MiniMax**.
