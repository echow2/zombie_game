from multiprocessing import Process, Pipe, Manager, Lock
from game.gui import run_gui
from game.player import player_process
from game.zombie import zombie_process
from shared.map_state import SharedMap

if __name__ == "__main__":
    width, height = 10, 10
    manager = Manager()

    shared_map_data = manager.list([
        manager.list([" " for _ in range(width)]) for _ in range(height)
    ])
    shared_lock = Lock()
    game_over = manager.Value("b", False)  # shared boolean

    map_data = SharedMap(shared_map_data, shared_lock, width, height)

    parent_conn_p, child_conn_p = Pipe()
    parent_conn_z, child_conn_z = Pipe()

    player = Process(
        target=player_process,
        args=(shared_map_data, shared_lock, width, height, child_conn_p, game_over)
    )

    zombie = Process(
        target=zombie_process,
        args=(shared_map_data, shared_lock, width, height, child_conn_z, game_over)
    )

    player.start()
    zombie.start()

    run_gui(map_data, parent_conn_p, parent_conn_z, game_over)

    player.join()
    zombie.join()
