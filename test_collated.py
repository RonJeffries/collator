import pytest

from collator import Collator
from result import Result


class TestCollated:
    def test_result(self):
        result = Result(name='TestBar', outcome='Fail', is_new=True)
        assert result.name == 'TestBar'
        assert result.outcome == 'Fail'
        assert result.is_new is True

    def test_collator_initialized(self):
        collator = Collator()
        assert list(collator.results()) == []

    def test_story_test(self):
        collator = Collator()
        assert collator.high_water == 0
        collator.add(name='TestFoo', outcome='Pass')
        collator.add(name='TestBar', outcome='Fail')
        initial_result = list(collator.results())
        self.check(initial_result, 0,
                   'TestFoo', 'Pass', True)
        self.check(initial_result, 1,
                   'TestBar', 'Fail', True)
        collator.add(name='TestBaz', outcome='Pass')
        assert collator.high_water == 2
        collator.add(name='TestBar', outcome='Pass')
        second_result = list(collator.results())
        self.check(second_result, 0,
                   'TestFoo', 'Unrun', False)
        self.check(second_result, 1,
                   'TestBar', 'Pass', False)
        self.check(second_result, 2,
                   'TestBaz', 'Pass', True)

    @staticmethod
    def check(results, index, name, outcome, new):
        result = results[index]
        assert result.name == name
        assert result.outcome == outcome
        assert result.is_new is new

    def test_with(self):
        collator = Collator()
        collator.add(name='TestFoo', outcome='Pass')
        collator.add(name='TestBar', outcome='Fail')
        initial_result = list(collator.results())
        collator.add(name='TestBaz', outcome='Pass')
        collator.add(name='TestBar', outcome='Pass')
        second_result = list(collator.results())

        self.check(initial_result, 0,
                   'TestFoo', 'Pass', True)
        self.check(initial_result, 1,
                   'TestBar', 'Fail', True)
        self.check(second_result, 0,
                   'TestFoo', 'Unrun', False)
        self.check(second_result, 1,
                   'TestBar', 'Pass', False)
        self.check(second_result, 2,
                   'TestBaz', 'Pass', True)

    def test_collator_aged_names(self):
        collator = Collator()
        collator.add(name='TestFoo', outcome='Pass')
        collator.add(name='TestBar', outcome='Fail')
        collator.results()
        collator.add(name='TestBaz', outcome='Pass')
        aged = list(collator.results())
        assert len(aged) == 3
        assert [a.name for a in aged] == ['TestFoo', 'TestBar', 'TestBaz']
        assert [a.is_new for a in aged] == [False, False, True]

    def test_key_order(self):
        d = dict()
        d['foo'] = 1
        d['bar'] = 2
        d['baz'] = 3
        assert list(d.keys()) == ['foo', 'bar', 'baz']
        d['bar'] = 20
        assert list(d.keys()) == ['foo', 'bar', 'baz']
        d['foo'] = 10
        d['mumble'] = 30
        assert list(d.keys()) == ['foo', 'bar', 'baz', 'mumble']
        assert list(d.values()) == [10, 20, 3, 30]

    def test_collator_without_with(self):
        collator = Collator()
        collator.add(name='TestFoo', outcome='Pass')
        collator.add(name='TestBar', outcome='Fail')
        initial_result = list(collator.results())

        self.check(initial_result, 0,
                   'TestFoo', 'Pass', True)
        self.check(initial_result, 1,
                   'TestBar', 'Fail', True)
        duplicate_initial_result = list(collator.results())
        assert duplicate_initial_result == initial_result

        collator.add(name='TestBaz', outcome='Pass')
        collator.add(name='TestBar', outcome='Pass')
        second_result = list(collator.results())

        self.check(second_result, 0,
                   'TestFoo', 'Unrun', False)
        self.check(second_result, 1,
                   'TestBar', 'Pass', False)
        self.check(second_result, 2,
                   'TestBaz', 'Pass', True)
        duplicate_second_result = list(collator.results())
        assert duplicate_second_result == second_result
