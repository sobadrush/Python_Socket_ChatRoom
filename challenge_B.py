import socket
import threading

# 1. 建立 UDP Socket 並綁定大門
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind(("0.0.0.0", 5001))
    sock.setblocking(False) # 設定為非阻塞模式，讓 recvfrom() 不會卡住整個程式
except OSError as e:
    print(f"無法綁定端口 5001: {e}")
    print("請檢查端口是否已被佔用")
    exit(1)


# 2. 定義「背景收信」的工作內容
def receive_messages():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"\n[收到來自 {addr[0]}]：{data.decode('utf-8')}")
        except BlockingIOError as e:
            # 【沒收到信】沒信也無所謂，裝作沒事繼續看電視（畫遊戲畫面）！
            print(f"接收訊息時發生錯誤: {e}")
            pass


# 召喚小精靈去背景執行 (與主程式分工合作)，daemon=True 代表這個小精靈會隨著主程式結束而自動消失，不會獨立存在。
threading.Thread(target=receive_messages, daemon=True).start()

# 3. 前景發信主程式
print("聊天室已啟動！請輸入訊息 (直接按 Enter 傳送)：")
# target_ip = "192.168.XXX.XXX" # [!請修改為同學的 IP]
target_ip = "127.0.0.1"  # [!請修改為同學的 IP]

try:
    while True:
        msg = input("")  # 這裡會卡住等你打字，但背景的 recvfrom() 依然在辛勤運作！
        try:
            sock.sendto(msg.encode("utf-8"), (target_ip, 5000))
        except socket.gaierror as e:
            print(f"IP 位址格式錯誤或網路問題: {e}")
        except OSError as e:
            print(f"網路錯誤: {e}")
        except Exception as e:
            print(f"發送訊息時發生未預期的錯誤: {e}")
except KeyboardInterrupt:
    print("\n聊天室已關閉")
finally:
    sock.close()
