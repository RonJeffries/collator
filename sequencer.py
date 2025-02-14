from aged_name import AgedName


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

    def aged_names(self):
        yield from self.yield_known_names()
        yield from self.yield_and_age_new_names()
        self.new_names = []

    def yield_known_names(self):
        for name in self.known_names:
            yield AgedName(name=name, is_new=False)

    def yield_and_age_new_names(self):
        for name in self.new_names:
            self.known_names.append(name)
            yield AgedName(name=name, is_new=True)
