import time
import numpy as np
from multiprocessing import shared_memory

def player_process(shm_name, width, height, conn, sem_key, game_over, score, lives):
    shm = shared_memory.SharedMemory(name=shm_name)
    grid = np.ndarray((height, width), dtype='S1', buffer=shm.buf)
    x, y = 0, 0
    grid[y][x] = b'P'

    while not game_over.value:
        if conn.poll():
            direction = conn.recv()
            nx, ny = x, y

            if direction == "UP":
                ny = max(0, y - 1)
            elif direction == "DOWN":
                ny = min(height - 1, y + 1)
            elif direction == "LEFT":
                nx = max(0, x - 1)
            elif direction == "RIGHT":
                nx = min(width - 1, x + 1)

            target = grid[ny][nx]

            if target == b'Z':
                lives.value -= 1
                print(f"[Player] Caught! Lives left: {lives.value}")
                if lives.value <= 0:
                    game_over.value = True
                    print("[Player] Game over.")
                else:
                    grid[y][x] = b' '
                    x, y = 0, 0
                    grid[y][x] = b'P'

            elif target == b'K':
                if sem_key.acquire(block=False):
                    print("[Player] Picked up key")
                    score.value += 1
                    grid[y][x] = b' '
                    x, y = nx, ny
                    grid[y][x] = b'P'
                    sem_key.release()

                    # Respawn key
                    import random
                    while True:
                        rx, ry = random.randint(0, width - 1), random.randint(0, height - 1)
                        if grid[ry][rx] == b' ':
                            grid[ry][rx] = b'K'
                            break

            elif target == b'H':
                if lives.value < 5:
                    lives.value += 1
                    print(f"[Player] Picked up heart! Lives: {lives.value}")
                else:
                    print("[Player] Picked up heart but already at max lives.")
                grid[y][x] = b' '
                x, y = nx, ny
                grid[y][x] = b'P'

                # Respawn heart
                import random
                while True:
                    rx, ry = random.randint(0, width - 1), random.randint(0, height - 1)
                    if grid[ry][rx] == b' ':
                        grid[ry][rx] = b'H'
                        break

            elif target == b' ':
                grid[y][x] = b' '
                x, y = nx, ny
                grid[y][x] = b'P'

        time.sleep(0.1)

    shm.close()
