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

## 聯絡方式
如有問題歡迎提出 issue 或聯絡專案維護者。
