import socket
import threading
import json
import pygame

pygame.init()

# 方格設定：10x10，每格 60 像素
GRID_SIZE = 10
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("座標同步 - 對手位置")
clock = pygame.time.Clock()

# UDP 接收/發送設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5001))
sock.setblocking(False)

# 對手位址（需手動設定或從接收到的資料取得）
TARGET_HOST = "127.0.0.1"
TARGET_PORT = 5000

# 玩家與敵人座標
player_x = 0
player_y = 0
enemy_x = None
enemy_y = None


def draw_grid():
    """繪製 10x10 方格線"""
    screen.fill((255, 255, 255))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def draw_player():
    """繪製玩家（藍色方塊）"""
    rect = pygame.Rect(player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, (0, 0, 255), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)


def draw_enemy():
    """繪製敵人（紅色方塊）"""
    if enemy_x is not None and enemy_y is not None:
        rect = pygame.Rect(
            enemy_x * CELL_SIZE, enemy_y * CELL_SIZE, CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(screen, (255, 0, 0), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)


def send_data():
    """發送玩家座標給對手"""
    global player_x, player_y
    while True:
        try:
            data = json.dumps({"x": player_x, "y": player_y}).encode()
            sock.sendto(data, (TARGET_HOST, TARGET_PORT))
        except Exception as e:
            print(f"發送錯誤: {e}")
        threading.Event().wait(0.1)


def receive_data():
    """接收對手發送的座標 JSON"""
    global enemy_x, enemy_y
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            enemy_package = json.loads(data.decode())
            enemy_x = enemy_package["x"]
            enemy_y = enemy_package["y"]
            print(f"收到對手座標: x={enemy_x}, y={enemy_y}")
        except BlockingIOError:
            pass
        except Exception as e:
            print(f"接收錯誤: {e}")


# 啟動接收與發送執行緒
recv_thread = threading.Thread(target=receive_data, daemon=True)
recv_thread.start()
send_thread = threading.Thread(target=send_data, daemon=True)
send_thread.start()

# 主遊戲迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 鍵盤控制玩家移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and player_x < GRID_SIZE - 1:
        player_x += 1
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and player_y < GRID_SIZE - 1:
        player_y += 1

    draw_grid()
    draw_player()
    draw_enemy()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
