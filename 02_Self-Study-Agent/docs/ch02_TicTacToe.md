# Chương 2: Tìm Kiếm Nhìn Trước (Look-Ahead Search) Trong Tic Tac Toe
*Nguyên tác: Chapter 2: Look-Ahead Search in Tic Tac Toe*
*Notebook gốc:* [ch02TicTacToe.ipynb](file:///d:/AlphaGoSimplified/ch02TicTacToe.ipynb)

---

## 1. Giới Thiệu Trò Chơi Tic Tac Toe & Ý Tưởng Nhìn Trước

Trong cờ ca-rô 3x3 (Tic Tac Toe), không gian bàn cờ có $3 \times 3 = 9$ ô. Hai người chơi lần lượt đánh dấu `X` hoặc `O`. Người đầu tiên tạo được 3 dấu thẳng hàng (ngang, dọc, chéo) sẽ thắng. Nếu bàn cờ kín mà không ai nối được 3 dấu, kết quả là hòa.

Ở chương này, chúng ta tiếp cận bằng phương pháp **Rule-Based Look-Ahead (Tìm kiếm nhìn trước theo luật cứng)**:
- **Nhìn trước 1 bước (Think 1 step ahead)**: Tìm xem có nước đi nào giúp ta thắng ngay lập tức không.
- **Nhìn trước 2 bước (Think 2 steps ahead)**: Chặn đối thủ nếu họ có thể thắng ở lượt tiếp theo.
- **Nhìn trước 3 bước (Think 3 steps ahead)**: Tạo ra thế đôi (gọng kìm / Fork) để đảm bảo sẽ thắng sau 3 nước.

---

## 2. Cài Đặt Các Thuật Toán Nhìn Trước

### 2.1. Nhìn trước 1 bước (`ttt_think1`)
Duyệt qua tất cả các ô hợp lệ (`env.validinputs`). Dùng `deepcopy` để đi thử:
```python
from copy import deepcopy

def ttt_think1(env):
    # Duyệt qua từng nước đi khả dĩ
    for m in env.validinputs:
        env_copy = deepcopy(env)
        state, reward, done, _ = env_copy.step(m)
        # Nếu nước đi này mang lại chiến thắng ngay lập tức
        if done and abs(reward) == 1:
            return m
    # Nếu không có nước thắng ngay, đi ngẫu nhiên
    return env.sample()
```

### 2.2. Nhìn trước 2 bước (`ttt_think2`)
Nếu không thắng ngay, kiểm tra xem đối thủ có thể thắng ở nước tiếp theo hay không. Nếu có, lập tức chiếm ô đó để chặn:
```python
def ttt_think2(env):
    # Bước 1: Kiểm tra xem ta có thắng ngay được không
    for m in env.validinputs:
        env_copy = deepcopy(env)
        state, reward, done, _ = env_copy.step(m)
        if done and abs(reward) == 1:
            return m
            
    # Bước 2: Nhìn trước 2 nước để chặn đối thủ
    for m1 in env.validinputs:
        for m2 in env.validinputs:
            if m1 != m2:
                env_copy = deepcopy(env)
                s, r, done, _ = env_copy.step(m1)
                s, r, done, _ = env_copy.step(m2)
                # Nếu nước m2 giúp đối thủ thắng, ta phải đánh vào m2
                if done and r != 0:
                    return m2
    return env.sample()
```

### 2.3. Nhìn trước 3 bước (`ttt_think3`)
Mô phỏng 3 lượt: ta đi `m1`, đối thủ đi `m2`, ta đi `m3`. Thu thập danh sách các nước `m1` dẫn đến chiến thắng ở nước thứ 3, và chọn nước `m1` có tần suất thắng cao nhất (tạo bẫy nhiều đường thắng nhất):
```python
def ttt_think3(env):
    # ... (kiểm tra 1 bước và 2 bước như trên) ...
    w3 = []
    for m1 in env.validinputs:
        for m2 in env.validinputs:
            for m3 in env.validinputs:
                if m1 != m2 and m1 != m3 and m2 != m3:
                    env_copy = deepcopy(env)
                    s, r, done, _ = env_copy.step(m1)
                    s, r, done, _ = env_copy.step(m2)
                    s, r, done, _ = env_copy.step(m3)
                    if done and r != 0:
                        w3.append(m1)
    if len(w3) > 0:
        return max(w3, key=w3.count)
    return env.sample()
```

---

## 3. So Sánh Hiệu Suất

| Thuật toán | Đấu với Random | Đấu với Think 1 | Đấu với Think 2 |
| :--- | :--- | :--- | :--- |
| **Think 1 Step** | Thắng ~80% | Hòa ~40%, Thắng ~40% | Bị áp đảo |
| **Think 2 Steps** | Thắng ~95% | Thắng ~85% | Cân bằng |
| **Think 3 Steps** | Thắng ~98% | Thắng ~90% | Thắng vượt trội |

### Hạn chế lớn:
Phương pháp này dùng các vòng lặp lồng nhau (`for` lồng 3 cấp). Nếu muốn nhìn trước 4, 5 hay 9 bước, code sẽ cực kỳ cồng kềnh, chậm chạp và dễ sinh lỗi. Đây chính là lý do chúng ta cần đến thuật toán **Đệ quy MiniMax** ở Chương 4!
