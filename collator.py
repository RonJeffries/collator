from result import Result
from typing import Generator, Self


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.high_water = 0

    def __enter__(self) -> Self:
        for name in self.outcomes.keys():
            self.outcomes[name] = 'Unrun'
        self.high_water = len(self.outcomes)
        return self

    def __exit__(self, *args):
        pass

    def add(self, name: str, outcome: str):
        self.outcomes[name] = outcome

    def results(self) -> Generator[Result, None, None]:
        return (Result(k, v, i>= self.high_water)
                for i, (k, v) in enumerate(self.outcomes.items()))
