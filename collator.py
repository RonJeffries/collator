from result import Result
from typing import Generator, Self


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.high_water = 0
        self.reset_on_add = self._prepare_for_next_batch

    def __enter__(self) -> Self:
        self._prepare_for_next_batch()
        return self

    def _prepare_for_next_batch(self):
        for name in self.outcomes.keys():
            self.outcomes[name] = 'Unrun'
        self.high_water = len(self.outcomes)

    def __exit__(self, *args):
        pass

    def add(self, name: str, outcome: str):
        self.outcomes[name] = outcome

    def results(self) -> Generator[Result, None, None]:
        return (Result(k, v, i>= self.high_water)
                for i, (k, v) in enumerate(self.outcomes.items()))
