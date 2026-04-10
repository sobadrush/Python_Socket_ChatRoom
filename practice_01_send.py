import socket

# AF_INET = IPv4 位址格式, SOCK_DGRAM = UDP 模式 (Datagram)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 把文字編成機器碼 bytes
message = "Hello 前方同學！".encode('utf-8')


# 發射！如果對方沒開接收端，用UDP傳送也不會閃退，信件會直接在虛空中消失。
target_info = ("127.0.0.1", 5000) # [!請修改為同學的 IP]
sock.sendto(message, target_info)
print("訊息已發送出去了！")