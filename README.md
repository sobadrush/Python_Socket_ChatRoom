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

## `sock.recvfrom()` 在 Windows 與 macOS 的錯誤處理差異

當 UDP Socket 設定為**非阻塞模式**（`sock.setblocking(False)`）且目前沒有資料可讀時，`recvfrom()` 的行為因作業系統而異：

| 作業系統 | 拋出的例外 | errno |
|---|---|---|
| macOS / Linux | `BlockingIOError` | `EAGAIN` / `EWOULDBLOCK` (11) |
| Windows | `OSError` | `WSAEWOULDBLOCK` (10035) |

> **注意**：`BlockingIOError` 是 `OSError` 的子類別，因此在 macOS/Linux 上兩者都可以捕捉到；但在 Windows 上只會拋出 `OSError`（errno 10035），必須另外處理。

### 跨平台建議寫法

```python
try:
    data, addr = sock.recvfrom(1024)
    # 處理收到的資料...
except BlockingIOError:
    # macOS / Linux：目前沒有資料可讀，忽略即可
    pass
except OSError as e:
    if e.errno == 10035:
        # Windows：WSAEWOULDBLOCK，目前沒有資料可讀，效果與 macOS/Linux 的 BlockingIOError 相同
        pass
    else:
        # 其他真正的網路錯誤才需要處理
        print(f"接收訊息時發生錯誤: {e}")
```

## 常見忽略檔
本專案已於 `.gitignore` 忽略 VSCode、macOS、IntelliJ、Python、uv、venv 等常見快取與環境檔案。

## 聯絡方式
如有問題歡迎提出 issue 或聯絡專案維護者。
