import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# "0.0.0.0" 代表此台電腦的任何網路介面都傾聽這個 5000 敲門聲
sock.bind(("0.0.0.0", 5000))
print("成功佔用 Port 5000，等待訊息中...")

# 一次最多接 1024 bytes 的包裹。這裡會「卡住(阻塞)」直到收到東西為止。
data, addr = sock.recvfrom(1024)

# 收到的資料也是 bytes，解碼顯示給人類看
text = data.decode('utf-8')
print(f"收到來自 {addr} 的訊息：", text)