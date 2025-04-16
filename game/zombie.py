from shared.map_state import SharedMap
import time
import random

def zombie_process(shared_list, lock, width, height, conn, game_over):
    shared_map = SharedMap(shared_list, lock, width, height)
    x, y = 9, 9
    shared_map.set(x, y, "Z")
    print("[Zombie] Started at (9,9)")

    while not game_over.value:
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        nx = max(0, min(width - 1, x + dx))
        ny = max(0, min(height - 1, y + dy))

        dest = shared_map.get(nx, ny)

        if dest == "P":
            print("[Zombie] Found the player! Game over.")
            game_over.value = True
            shared_map.set(x, y, " ")
            shared_map.set(nx, ny, "Z")
            x, y = nx, ny
        elif dest == " ":
            shared_map.set(x, y, " ")
            shared_map.set(nx, ny, "Z")
            x, y = nx, ny
            print(f"[Zombie] Moved to ({x},{y})")
        time.sleep(0.5)

    print("[Zombie] Game over. Exiting.")
