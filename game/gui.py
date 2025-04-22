import tkinter as tk
import numpy as np
from multiprocessing import shared_memory
import time

def run_gui(shm_name, width, height, conn, game_over, score, lives, start_time):
    root = tk.Tk()
    root.title("Zombie Escape")
    canvas = tk.Canvas(root, width=width * 40, height=height * 40)
    canvas.pack()

    score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
    score_label.pack()

    time_label = tk.Label(root, text="Time Left: 05:00", font=("Arial", 14))
    time_label.pack()

    lives_label = tk.Label(root, text="❤️❤️❤️❤️❤️", font=("Arial", 18))
    lives_label.pack()

    shm = shared_memory.SharedMemory(name=shm_name)
    grid = np.ndarray((height, width), dtype='S1', buffer=shm.buf)

    def send_command(cmd):
        conn.send(cmd)

    root.bind("<Up>", lambda e: send_command("UP"))
    root.bind("<Down>", lambda e: send_command("DOWN"))
    root.bind("<Left>", lambda e: send_command("LEFT"))
    root.bind("<Right>", lambda e: send_command("RIGHT"))

    def draw():
        if game_over.value:
            print("[GUI] Game over. Closing window.")
            root.destroy()
            return

        canvas.delete("all")
        for y in range(height):
            for x in range(width):
                val = grid[y][x]
                color = {
                b'P': "green",
                b'Z': "red",
                b'K': "yellow",
                b'H': "pink",
                b' ': "black"
            }.get(val, "gray")
                canvas.create_rectangle(
                    x * 40, y * 40, (x + 1) * 40, (y + 1) * 40,
                    fill=color, outline="white"
                )

        score_label.config(text=f"Score: {score.value}")
        hearts = "❤️" * lives.value + "🖤" * (5 - lives.value)
        lives_label.config(text=hearts)


        elapsed = int(time.time() - start_time)
        remaining = max(0, 300 - elapsed)
        minutes, seconds = divmod(remaining, 60)
        time_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")

        root.after(100, draw)

    draw()
    root.mainloop()
    shm.close()
