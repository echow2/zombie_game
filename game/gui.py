import tkinter as tk
import numpy as np
from multiprocessing import shared_memory
import time
from PIL import Image, ImageTk


def run_gui(shm_name, width, height, conn, game_over, score, lives, start_time):
    root = tk.Tk()
    root.title("Zombie Escape")
    canvas = tk.Canvas(root, width=width * 40, height=height * 40)
    canvas.pack()

    # Load item sprites
    key_sprite = ImageTk.PhotoImage(Image.open("sprites/items/key.png").resize((40, 40)))
    heart_sprite = ImageTk.PhotoImage(Image.open("sprites/items/heart.png").resize((40, 40)))

    score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
    score_label.pack()

    time_label = tk.Label(root, text="Time Left: 05:00", font=("Arial", 14))
    time_label.pack()

    lives_label = tk.Label(root, text="❤️❤️❤️❤️❤️", font=("Arial", 18))
    lives_label.pack()

    shm = shared_memory.SharedMemory(name=shm_name)
    grid = np.ndarray((height, width), dtype='S1', buffer=shm.buf)

    # === LOAD SPRITES ===

    # Load zombie walk frames
    zombie_frame_paths = [
        "sprites/zombie/Walk1.png",
        "sprites/zombie/Walk2.png",
        "sprites/zombie/Walk3.png",
        "sprites/zombie/Walk4.png",
        "sprites/zombie/Walk5.png",
        "sprites/zombie/Walk6.png",

    ]
    zombie_frames = [ImageTk.PhotoImage(Image.open(path).resize((40, 40))) for path in zombie_frame_paths]

    # Extract single frame from player sprite sheet (front standing pose)
    player_sheet = Image.open("sprites/player/Unarmed_Walk_full.png")
    tile_width = player_sheet.width // 3
    tile_height = player_sheet.height // 4
    player_frame = ImageTk.PhotoImage(player_sheet.crop((tile_width, 0, tile_width * 2, tile_height)).resize((40, 40)))

    # Keep references alive
    image_refs = zombie_frames + [player_frame]

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
        frame_idx = (int(time.time() * 10) % len(zombie_frames))

        for y in range(height):
            for x in range(width):
                val = grid[y][x]
                if val == b'P':
                    canvas.create_image(x * 40, y * 40, anchor=tk.NW, image=player_frame)
                elif val == b'Z':
                    canvas.create_image(x * 40, y * 40, anchor=tk.NW, image=zombie_frames[frame_idx])
                elif val == b'K':
                    canvas.create_image(x * 40, y * 40, anchor=tk.NW, image=key_sprite)
                elif val == b'H':
                    canvas.create_image(x * 40, y * 40, anchor=tk.NW, image=heart_sprite)
                else:
                    canvas.create_rectangle(
                        x * 40, y * 40, (x + 1) * 40, (y + 1) * 40,
                        fill="black", outline="white"
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
