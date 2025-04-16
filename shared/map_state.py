class SharedMap:
    def __init__(self, shared_list, lock, width, height):
        self.map = shared_list
        self.lock = lock
        self.width = width
        self.height = height

    def set(self, x, y, val):
        with self.lock:
            self.map[y][x] = val

    def get(self, x, y):
        with self.lock:
            return self.map[y][x]
