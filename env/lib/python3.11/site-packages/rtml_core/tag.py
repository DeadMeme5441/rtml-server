class Tag:
    def __init__(self, name, start_position=None):
        self.name = name

        if start_position is None:
            self.start_positions = []
        else:
            self.start_positions = [start_position]

        self.end_positions = []
        self.pairs = []

    def __dict__(self):
        return {
            "name": self.name,
            "start_positions": self.start_positions,
            "end_positions": self.end_positions,
            "pairs": self.pairs,
        }

    def add_start_position(self, position):
        self.start_positions.append(position)

    def add_end_position(self, position):
        self.end_positions.append(position)

    def enclosing_pairs(self):
        self.pairs = list(zip(self.start_positions, self.end_positions))

    def __repr__(self):
        return f"name: {self.name} pairs: {self.pairs}"
