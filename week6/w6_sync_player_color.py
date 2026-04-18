import socket
import json
import pygame
import sys
import random

# === 1. 面板與網路初始化 ===
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Week 6 - 雙人座標同步 + 色彩同步")
clock = pygame.time.Clock()

my_x, my_y = 100, 100
enemy_x, enemy_y = -100, -100  # 一開始對方在畫面外

# 背景顏色
bg_color = (30, 30, 50)  # 預設深色背景
enemy_bg_color = (30, 30, 50)

# 奇異顏色列表
WEIRD_COLORS = [
    (255, 192, 203),  # 粉紅
    (255, 255, 0),    # 亮黃
    (0, 255, 127),    # 春綠
    (255, 165, 0),    # 橙色
    (138, 43, 226),   # 藍紫
    (255, 20, 147),   # 深粉
    (0, 191, 255),    # 深天藍
    (255, 69, 0),     # 紅橙
]

# 建立 UDP 連線
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

# 【關鍵】：設定為非阻塞模式 Non-blocking !!!
sock.setblocking(False)

# 測試用：請輸入同學的 IP，如果沒有同學可改為 "127.0.0.1" 測試自己傳給自己
TARGET_IP = input("請輸入對方 IP (Enter 預設 127.0.0.1): ")
if not TARGET_IP:
    TARGET_IP = "127.0.0.1"

print(f"連線成功！準備將座標同步給 {TARGET_IP}")

# === 2. 遊戲主迴圈 ===
while True:
    screen.fill(enemy_bg_color)

    # --- A. 接收對方的資料 ---
    try:
        data, addr = sock.recvfrom(1024)

        # 拆開看對方傳了什麼
        enemy_package = json.loads(data.decode())
        enemy_x = enemy_package['x']
        enemy_y = enemy_package['y']

        # 接收對方的背景顏色
        if 'bg' in enemy_package:
            enemy_bg_color = tuple(enemy_package['bg'])

    except BlockingIOError:
        # 沒有信？當作沒發生，程式繼續往下走！
        pass
    except json.JSONDecodeError:
        # 防止有人亂傳不是 JSON 格式的垃圾訊息導致閃退
        pass

    # --- B. 處理遊戲事件與玩家輸入 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 按空白鍵隨機改變背景顏色
                bg_color = random.choice(WEIRD_COLORS)

    # 鍵盤控制自己移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  my_x -= 5
    if keys[pygame.K_RIGHT]: my_x += 5
    if keys[pygame.K_UP]:    my_y -= 5
    if keys[pygame.K_DOWN]:  my_y += 5

    # --- C. 繪圖階段 ---
    # 畫自己 (藍色)
    pygame.draw.rect(screen, (59, 130, 246), (my_x, my_y, 40, 40))
    # 畫對手 (綠色)
    pygame.draw.rect(screen, (16, 185, 129), (enemy_x, enemy_y, 40, 40))

    pygame.display.flip()
    clock.tick(60)

    # --- D. 送出自己的資料給對方 ---
    my_package = {
        "x": my_x,
        "y": my_y,
        "bg": list(bg_color)  # 將背景顏色轉為 list 方便 JSON 序列化
    }

    # 打包 -> 轉 bytes -> 送出
    json_str = json.dumps(my_package)
    try:
        sock.sendto(json_str.encode(), (TARGET_IP, 5000))
    except OSError:
        # 若發生網路短暫斷線引發的 OS 錯誤，我們也能忽略不處理以避免閃退
        pass
