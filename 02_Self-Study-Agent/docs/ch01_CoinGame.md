# Chương 1: Rule-Based AI Trong Trò Chơi Bốc Xu (Coin Game)
*Nguyên tác: Chapter 1: Rule-Based AI in the Coin Game*
*Notebook gốc:* [ch01CoinGame.ipynb](file:///d:/AlphaGoSimplified/ch01CoinGame.ipynb)

---

> *"Can you learn stuff you haven't been programmed with so you can be, you know, more human?"*
> — **John Connor hỏi Kẻ Hủy Diệt (Terminator 2: Judgement Day)**

Câu hỏi kinh điển này phản ánh hai trường phái đối lập trong Trí tuệ nhân tạo (AI):
1. **Rule-Based AI (AI dựa trên luật)**: Con người lập trình sẵn toàn bộ quy tắc cứng nhắc và bảo cỗ máy phải làm gì trong từng trường hợp.
2. **Machine Learning (Học máy - ML)**: Cho máy tính xem hàng triệu ví dụ và để nó tự tìm ra quy luật ngầm.

Trong chương mở đầu này, bạn sẽ làm quen với trò chơi đầu tiên: **Last Coin Standing (Trò chơi bốc xu)** và tạo ra một AI dựa trên luật có tỷ lệ thắng tuyệt đối 100% khi đi sau!

---

## 1. Luật Chơi & Chiến Thuật Bất Bại

### 1.1. Luật chơi Last Coin Standing
- Có một đống gồm **21 đồng xu** trên bàn.
- Hai người chơi thay phiên nhau bốc xu.
- Mỗi lượt, người chơi chỉ được phép bốc **1 hoặc 2 đồng xu**.
- **Người bốc được đồng xu cuối cùng là người chiến thắng**.

### 1.2. Chiến thuật toán học để luôn thắng 100%
Đây là trò chơi có tổng số xu mỗi lượt tối đa là $1 + 2 = 3$. Quy tắc vàng là đưa số xu còn lại về **bội số của 3** ($0, 3, 6, 9, 12, 15, 18, 21$):
- Ban đầu có 21 đồng xu ($21 \equiv 0 \pmod 3$).
- Nếu bạn đi thứ 2 (Player 2):
  - Khi đối thủ bốc 1 đồng $\rightarrow$ Số xu còn lại chia 3 dư 2 $\rightarrow$ Bạn bốc 2 đồng để đưa về bội số của 3.
  - Khi đối thủ bốc 2 đồng $\rightarrow$ Số xu còn lại chia 3 dư 1 $\rightarrow$ Bạn bốc 1 đồng để đưa về bội số của 3.
  - Bằng cách này, bạn luôn đưa trạng thái về bội số của 3 sau mỗi lượt của mình. Đến cuối ván, đối thủ buộc phải để lại 1 hoặc 2 đồng, và bạn sẽ bốc hết để giành chiến thắng!

---

## 2. Cài Đặt Mã Nguồn Python

### 2.1. Hàm Rule-Based AI hoàn hảo
```python
def rule_based_AI(env):
    """
    Chiến thuật chơi hoàn hảo:
    - Nếu số xu còn lại (env.state) không chia hết cho 3:
      Bốc đúng phần dư (env.state % 3) để đưa bàn cờ về bội số của 3.
    - Nếu đã là bội số của 3 (rơi vào thế bất lợi):
      Bốc ngẫu nhiên (chờ đối thủ phạm sai lầm).
    """
    if env.state % 3 != 0:
        move = env.state % 3
    else:
        move = env.sample()
    return move
```

### 2.2. Hàm mô phỏng ván đấu hoàn chỉnh
```python
def one_coin_game(player1, player2):
    env = coin_game()
    while True:
        # Lượt người chơi 1
        m1 = player1(env)
        s, r, done, _ = env.step(m1)
        if done:
            return 1  # Player 1 thắng
        
        # Lượt người chơi 2
        m2 = player2(env)
        s, r, done, _ = env.step(m2)
        if done:
            return 2  # Player 2 thắng
```

---

## 3. Kết Quả Thử Nghiệm

Khi cho `rule_based_AI` thi đấu với `random_player` trong 1,000 ván:
- **Khi AI đi trước (Player 1)**: Tỷ lệ thắng khoảng **67%** (do nếu ban đầu bốc sai, đối thủ ngẫu nhiên có thể vô tình đưa về thế có lợi).
- **Khi AI đi sau (Player 2)**: Tỷ lệ thắng đạt **100% tuyệt đối** (không bao giờ thua dù chỉ 1 ván).

---

## 4. Tầm Quan Trọng Đối Với Các Chương Sau
Rule-Based AI phát triển trong chương này đóng 3 vai trò chiến lược:
1. **Chuẩn đánh giá (Benchmark)**: Dùng để kiểm tra độ thông minh của các mô hình MiniMax, MCTS, Q-Learning và Deep RL ở các chương sau.
2. **Sinh dữ liệu chuyên gia**: Dùng để chơi tự động tạo dữ liệu mẫu (kinh nghiệm chơi hoàn hảo) phục vụ huấn luyện mạng nơ-ron (Deep Learning).
3. **Minh chứng**: Thấy rõ sức mạnh của AI dựa trên luật khi không gian trò chơi nhỏ và luật chơi toán học rõ ràng.
