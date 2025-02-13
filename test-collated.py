import pytest


class Status:
    def __init__(self, name: str, outcome: str):
        self.name = name
        self.outcome = outcome


class TestCollated:
    def test_status(self):
        status = Status('TestFoo', 'Pass')
        assert status.name == 'TestFoo'
        assert status.outcome == 'Pass'