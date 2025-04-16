import tkinter as tk

def run_gui(shared_map, conn_p, conn_z, game_over):
    root = tk.Tk()
    root.title("🧟 Zombie Escape")

    grid_size = shared_map.width
    cell_size = 40

    canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size, bg='black')
    canvas.pack()

    def send_move(direction):
        print(f"[GUI] Sending move: {direction}")
        conn_p.send(direction)

    root.bind("<Up>", lambda event: send_move("UP"))
    root.bind("<Down>", lambda event: send_move("DOWN"))
    root.bind("<Left>", lambda event: send_move("LEFT"))
    root.bind("<Right>", lambda event: send_move("RIGHT"))

    def update_gui():
        if game_over.value:
            print("[GUI] Game over! Closing window.")
            root.destroy()
            return

        canvas.delete("all")
        for y in range(grid_size):
            for x in range(grid_size):
                val = shared_map.get(x, y)
                if val == " ":
                    continue
                color = (
                    "green" if val == "P"
                    else "red" if val == "Z"
                    else "gray"
                )
                canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color,
                    outline="white"
                )
        root.after(100, update_gui)

    update_gui()
    root.mainloop()
