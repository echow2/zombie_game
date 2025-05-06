Zombie Escape - OS Game Project README
Demo Link
https://youtu.be/VBOse89Sf5k
Requirements
Python 3.8, tkinter, numpy

Game Title
Zombie Escape
Game Summary
Zombie Escape is a real-time, grid-based survival game where the player must evade multiple patrolling zombies while collecting scattered keys to earn points. The game is designed to demonstrate core operating system concepts like process management, inter-process communication shared memory, and synchronization in an engaging and interactive format. The player starts with 5 lives and navigates a 10x10 grid, avoiding zombies and collecting power-ups like hearts to restore lives. The game ends either when the player loses all lives or survives a full 5-minute countdown.
Core Gameplay Loop
The player uses arrow keys to move around the grid. Each turn, the player checks the cell theyre about to move into: if it's a key (K), they gain a point and the key respawns elsewhere; if it's a heart (H), they gain a life (up to 5 max); if it's a zombie (Z), they lose a life. Zombies move randomly in the background as separate processes, creating the need for constant awareness and evasion. The GUI updates in real-time to reflect map changes, player status, lives, and a countdown timer. The challenge escalates with more zombies appearing, creating a fast-paced loop of risk, reward, and survival under OS-level mechanics.

Controls
Arrow Keys: Move the player (Up, Down, Left, Right)
Zombie Escape - OS Game Project README
Core Mechanics
Key collection (+1 score)
Heart pickups (+1 life, max 5)
Zombie evasion (collision = -1 life)
Lives shown as heart icons
Time limit: 5 minutes
Narrative
You are the last human survivor in a zombie-overrun lab. You must collect critical supplies (keys) and survive
long enough for extraction. Each heart you find boosts your will to live but one bite could be your last...
OS Concepts Used
1. Process Creation: Player and zombies run as separate multiprocessing.Process instances
2. Shared Memory: Game map is stored in a shared_memory.SharedMemory block accessed by all
components
3. Interprocess Communication (Pipe): GUI sends player movement commands to the player process through
multiprocessing.Pipe()
4. Synchronization: Player uses multiprocessing.Semaphore to lock key pickups and prevent race conditions
5. Threading: Each zombie runs its logic in a threading.Thread to simulate concurrent enemy AI
6. Timer: A separate threading.Thread tracks time and ends the game after 5 minutes
7. File I/O: Game score is appended to high_scores.txt upon game over
Code Examples
main.py
Process Creation:
player = Process(target=player_process, args=(...))
zombie = Process(target=zombie_process, args=(...))
player.start()
zombie.start()
Zombie Escape - OS Game Project README
Shared Memory:
shm = shared_memory.SharedMemory(create=True, size=WIDTH * HEIGHT)
grid = np.ndarray((HEIGHT, WIDTH), dtype='S1', buffer=shm.buf)
Inter-Process Communication (Pipe):
parent_conn, child_conn = Pipe()
...
conn.send("UP")
Timer Thread:
def end_game_after_5_min(game_over):
time.sleep(300)
game_over.value = True
File I/O:
with open("high_scores.txt", "a") as f:
f.write(f"{timestamp} - Score: {score.value}\n")
player.py
Synchronization (Semaphore):
if sem_key.acquire(block=False):
score.value += 1
sem_key.release()
zombie.py
Threading (Zombie AI):
t = threading.Thread(target=zombie_ai, args=(...))
t.start()
Next Steps
Zombie Escape - OS Game Project README
Next steps for the Zombie Escape project include enhancing both gameplay and visual fidelity. A key visual upgrade will involve replacing the current color-coded blocks with actual character sprites or images representing the player and zombies. This will make the game feel more animated and immersive. On the technical side, planned improvements include smarter zombie AI using pathfinding algorithms, introducing multiple difficulty levels, and simulating OS-level challenges such as resource deadlock or starvation. Additional polish, such as sound effects, animations, and persistent high score tracking, will also be considered to round out the final demo experience.