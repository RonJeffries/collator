
from aged_name import AgedName
from result import Result
from sequencer import Sequencer


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.sequencer = Sequencer()

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, *args):
        pass

    def begin(self):
        self.sequencer.begin()
        self.outcomes = dict()

    def add(self, name:str, outcome:str):
        self.outcomes[name] = outcome
        self.add_name(name)

    def add_name(self, name:str):
        self.sequencer.add_name(name)

    def aged_names(self):
        yield from self.sequencer.aged_names()

    def outcome_for(self, name:str):
        try:
            return self.outcomes[name]
        except KeyError:
            return 'Unrun'

    def result_for(self, name:str, is_new:bool):
        return Result(name=name, outcome=(self.outcome_for(name)), is_new=is_new)

    def results(self):
        for aged_name in self.aged_names():
            yield self.result_for(aged_name.name, is_new=aged_name.is_new)

