from shared.map_state import SharedMap
import time

def player_process(shared_list, lock, width, height, conn, game_over):
    shared_map = SharedMap(shared_list, lock, width, height)
    x, y = 0, 0
    shared_map.set(x, y, "P")
    print("[Player] Started at (0,0)")

    while not game_over.value:
        if conn.poll():
            direction = conn.recv()
            print(f"[Player] Received direction: {direction}")
            new_x, new_y = x, y

            if direction == "UP":
                new_y = max(0, y - 1)
            elif direction == "DOWN":
                new_y = min(height - 1, y + 1)
            elif direction == "LEFT":
                new_x = max(0, x - 1)
            elif direction == "RIGHT":
                new_x = min(width - 1, x + 1)

            dest = shared_map.get(new_x, new_y)
            if dest == "Z":
                print("[Player] Eaten by zombie!")
                game_over.value = True
            elif dest == " ":
                shared_map.set(x, y, " ")
                shared_map.set(new_x, new_y, "P")
                x, y = new_x, new_y
                print(f"[Player] Moved to ({x},{y})")
        time.sleep(0.05)

    print("[Player] Game over. Exiting.")
