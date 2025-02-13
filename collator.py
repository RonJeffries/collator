from aged_name import AgedName


class Collator:
    def __init__(self):
        self.new_names = []
        self.known_names = []

    def begin(self):
        pass

    def add_name(self, name:str):
        if name not in self.known_names and name not in self.new_names:
            self.new_names.append(name)

    def aged_names(self):
        known = self.known_names[:]
        while known:
            name = known.pop(0)
            yield AgedName(name=name, is_new=False)
        while self.new_names:
            name = self.new_names.pop(0)
            self.known_names.append(name)
            yield AgedName(name=name, is_new=True)


    def results(self):
        return []
