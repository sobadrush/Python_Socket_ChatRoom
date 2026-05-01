# Python Socket ChatRoom

本專案為一個基於 Python 的 Socket 聊天室練習與測試範例，適合學習網路程式設計、Socket 通訊、多執行緒應用等主題。

## 目錄結構
- `challenge_A.py`、`challenge_B.py`：進階練習題範例
- `multi_thread_test.py`：多執行緒測試程式
- `practice_01_send.py`、`practice_01_receive.py`：基本 Socket 傳送/接收練習

## 執行環境
- Python 3.10 以上
- 建議使用虛擬環境（venv/uv）管理套件

## 快速開始
1. 建立虛擬環境並安裝依賴（如有）：
   ```sh
   uv venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # 若有需求檔
   ```
2. 執行範例程式：
   ```sh
   python practice_01_send.py
   python practice_01_receive.py
   ```

## 常見忽略檔
本專案已於 `.gitignore` 忽略 VSCode、macOS、IntelliJ、Python、uv、venv 等常見快取與環境檔案。

## 跨平台注意事項：非阻塞模式下的例外處理差異

在使用 `sock.setblocking(False)` 設定 UDP Socket 為非阻塞模式後，呼叫 `recvfrom()` 時，各平台的例外行為不盡相同。

### 平台差異說明

| 平台 | 沒有資料可讀時 | 收到 ICMP「目的地不可達」時 |
|------|--------------|--------------------------|
| Linux / macOS | 拋出 `BlockingIOError` | 靜默忽略，下次 `sendto()` 才回傳 `-1`（errno: `ECONNREFUSED`）|
| **Windows** | 拋出 `BlockingIOError` | **主動拋出 `ConnectionResetError` (WinError 10054)** |

> Windows 的 TCP/IP stack 會主動將 ICMP 訊息傳遞給應用程式，  
> 而 Linux / macOS 通常將此訊息降級為安靜忽略。

### 跨平台正確寫法

若要讓程式在 Linux、macOS、Windows 上都能正常運作，`recvfrom()` 的例外處理需同時捕捉兩種例外：

```python
# ✅ 跨平台寫法：同時處理 Linux/macOS 與 Windows
try:
    data, addr = sock.recvfrom(1024)
    enemy_package = json.loads(data.decode())
    enemy_x = enemy_package['x']
    enemy_y = enemy_package['y']
except (BlockingIOError, ConnectionResetError):
    # 無資料時或 ICMP 回應時，正常忽略繼續執行
    pass
except json.JSONDecodeError:
    # 忽略格式錯誤的封包
    pass
```

本專案中 `challenge_A.py`、`challenge_B.py`、`week6/` 下各同步程式均已採用此寫法。

## 聯絡方式
如有問題歡迎提出 issue 或聯絡專案維護者。
