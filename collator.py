from result import Result
from sequencer import Sequencer
from typing import Generator, Self


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.sequencer = Sequencer()

    def __enter__(self) -> Self:
        self.sequencer._testing_begin()
        for name in self.outcomes.keys():
            self.outcomes[name] = 'Unrun'
        return self

    def __exit__(self, *args):
        pass

    def add(self, name: str, outcome: str):
        self.outcomes[name] = outcome
        self.sequencer.add_name(name)

    def results(self) -> Generator[Result, None, None]:
        return (self._result_for(aged_name.name, aged_name.is_new)
                for aged_name in self.sequencer.aged_names())

    def _result_for(self, name: str, is_new: bool)-> Result:
        return Result(name, self._outcome_for(name), is_new)

    def _outcome_for(self, name: str) -> str:
        return self.outcomes.get(name, "Unrun")
