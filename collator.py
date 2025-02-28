from result import Result
from typing import Generator, Self


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.high_water = 0
        self.reset_on_add = self._prepare_for_next_batch

    def add(self, name: str, outcome: str):
        self.reset_on_add()
        self.outcomes[name] = outcome

    def results(self) -> Generator[Result, None, None]:
        self.reset_on_add = self._prepare_for_next_batch
        return (Result(k, v, i>= self.high_water)
                for i, (k, v) in enumerate(self.outcomes.items()))

    def _prepare_for_next_batch(self):
        for name in self.outcomes.keys():
            self.outcomes[name] = 'Unrun'
        self.high_water = len(self.outcomes)
        self.reset_on_add = lambda: None
