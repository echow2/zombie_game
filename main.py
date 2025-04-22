from multiprocessing import Process, Semaphore, Value, Pipe, shared_memory
import numpy as np
import threading
import time
from game.gui import run_gui
from game.player import player_process
from game.zombie import zombie_process

WIDTH, HEIGHT = 10, 10

def spawn_keys(grid, count):
    import random
    for _ in range(count):
        while True:
            x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
            if grid[y][x] == b' ':
                grid[y][x] = b'K'
                break

def end_game_after_5_min(game_over):
    time.sleep(300)
    game_over.value = True
    print("[Timer] 5 minutes passed. Game over!")

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(create=True, size=WIDTH * HEIGHT)
    grid = np.ndarray((HEIGHT, WIDTH), dtype='S1', buffer=shm.buf)
    grid[:] = b' '

    # Spawn 3 keys
    spawn_keys(grid, 3)

    key_lock = Semaphore(1)
    game_over = Value("b", False)
    score = Value("i", 0)
    lives = Value("i", 5)
    parent_conn, child_conn = Pipe()

    timer_thread = threading.Thread(target=end_game_after_5_min, args=(game_over,))
    timer_thread.start()

    player = Process(target=player_process, args=(shm.name, WIDTH, HEIGHT, child_conn, key_lock, game_over, score, lives))
    player.start()

    # Spawn 3 zombies
    zombie_threads = []
    for i in range(2):
        z = Process(target=zombie_process, args=(shm.name, WIDTH, HEIGHT, game_over, i))
        z.start()
        zombie_threads.append(z)

    run_gui(shm.name, WIDTH, HEIGHT, parent_conn, game_over, score, lives, time.time())

    player.join()
    for z in zombie_threads:
        z.join()

    # Save score
    import datetime
    with open("high_scores.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - Score: {score.value}\n")

    shm.close()
    shm.unlink()
