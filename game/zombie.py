import time, random, threading
import numpy as np
from multiprocessing import shared_memory

def zombie_ai(shm_name, width, height, game_over, seed_offset):
    random.seed(time.time() + seed_offset)
    shm = shared_memory.SharedMemory(name=shm_name)
    grid = np.ndarray((height, width), dtype='S1', buffer=shm.buf)

    # Find empty spot for zombie
    while True:
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        if grid[y][x] == b' ':
            grid[y][x] = b'Z'
            break

    while not game_over.value:
        dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
        nx, ny = max(0, min(width - 1, x + dx)), max(0, min(height - 1, y + dy))

        if grid[ny][nx] == b'P':
            print("[Zombie] Got player!")
            grid[y][x] = b' '
            grid[ny][nx] = b'Z'
            game_over.value = False  # Let player decide based on lives
            x, y = nx, ny
        elif grid[ny][nx] == b' ':
            grid[y][x] = b' '
            grid[ny][nx] = b'Z'
            x, y = nx, ny

        time.sleep(0.5)

    shm.close()

def zombie_process(shm_name, width, height, game_over, seed_offset):
    t = threading.Thread(target=zombie_ai, args=(shm_name, width, height, game_over, seed_offset))
    t.start()
    t.join()
