import socket
import threading

# 1. 建立 UDP Socket 並綁定大門
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

# 2. 定義「背景收信」的工作內容
def receive_messages():
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"\n[收到來自 {addr[0]}]：{data.decode('utf-8')}")

# 召喚小精靈去背景執行 (與主程式分工合作)，daemon=True 代表這個小精靈會隨著主程式結束而自動消失，不會獨立存在。
threading.Thread(target=receive_messages, daemon=True).start()

# 3. 前景發信主程式
print("聊天室已啟動！請輸入訊息 (直接按 Enter 傳送)：")
# target_ip = "192.168.XXX.XXX" # [!請修改為同學的 IP]
target_ip = "127.0.0.1" # [!請修改為同學的 IP]

while True:
    msg = input("")  # 這裡會卡住等你打字，但背景的 recvfrom() 依然在辛勤運作！
    sock.sendto(msg.encode('utf-8'), (target_ip, 5001))