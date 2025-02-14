from aged_name import AgedName
from typing import Generator


class Sequencer:
    def __init__(self):
        self.new_names = []
        self.known_names = []

    def add_name(self, name: str):
        if name not in self.known_names and name not in self.new_names:
            self.new_names.append(name)

    def aged_names(self) -> Generator[AgedName, None, None]:
        yield from self._yield_known_names()
        yield from self._yield_and_age_new_names()
        self.new_names = []

    def _yield_known_names(self) -> Generator[AgedName, None, None]:
        for name in self.known_names:
            yield AgedName(name=name, is_new=False)

    def _yield_and_age_new_names(self) -> Generator[AgedName, None, None]:
        for name in self.new_names:
            self.known_names.append(name)
            yield AgedName(name=name, is_new=True)

    def _testing_begin(self):
        self.known_names.extend(self.new_names)
        self.new_names = []
