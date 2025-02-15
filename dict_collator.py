from result import Result


class DictCollator:
    def __init__(self):
        self.collator = dict()
        self.high_water = 0

    def __enter__(self):
        self.high_water = len(self.collator)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add(self, name, outcome):
        self.collator[name] = outcome

    def results(self):
        return [Result(name, outcome, i>=self.high_water)
            for i, (name, outcome) in enumerate(self.collator.items())]
