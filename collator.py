from result import Result
from sequencer import Sequencer
from typing import Generator, Self


class Collator:
    def __init__(self):
        self.outcomes = dict()
        self.sequencer = Sequencer()

    def __enter__(self) -> Self:
        self._testing_begin()
        return self

    def __exit__(self, *args):
        pass

    def add(self, name: str, outcome: str):
        self.outcomes[name] = outcome
        self.sequencer.add_name(name)

    def results(self) -> Generator[Result, None, None]:
        return (self._result_for(aged_name.name, is_new=aged_name.is_new)
                for aged_name in self.sequencer.aged_names())

    def _result_for(self, name: str, is_new: bool)-> Result:
        return Result(name=name, outcome=(self._outcome_for(name)), is_new=is_new)

    def _outcome_for(self, name: str) -> str:
        try:
            return self.outcomes[name]
        except KeyError:
            return 'Unrun'

    # noinspection PyProtectedMember
    def _testing_begin(self):
        self.sequencer._testing_begin()
        self.outcomes = dict()

