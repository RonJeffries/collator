from collections import defaultdict

from aged_name import AgedName
from result import Result
from status import Status


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.new_names = []
        self.known_names = []

    def begin(self):
        self.known_names.extend(self.new_names)
        self.new_names = []
        self.outcomes = defaultdict()

    def add(self, name:str, outcome:str):
        self.outcomes[name] = outcome

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

    def result_for(self, name: str, is_new):
        return Result(name=name, outcome=(self.outcome_for(name)), is_new=is_new)

    def outcome_for(self, name):
        try:
            return self.outcomes[name]
        except KeyError:
            return 'Unrun'

    def results(self):
        return []
