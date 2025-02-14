
class Sequencer:
    def __init__(self):
        self.new_names = []
        self.known_names = []

    def begin(self):
        self.known_names.extend(self.new_names)
        self.new_names = []

    def add_name(self, name:str):
        if name not in self.known_names and name not in self.new_names:
            self.new_names.append(name)
