import pytest

from aged_name import AgedName
from collator import Collator
from result import Result
from sequencer import Sequencer


class TestCollated:
    def test_result(self):
        result = Result(name='TestBar', outcome='Fail', is_new=True)
        assert result.name == 'TestBar'
        assert result.outcome == 'Fail'
        assert result.is_new is True

    def test_collator_initialized(self):
        collator = Collator()
        collator.begin()
        assert list(collator.results()) == []

    def test_added_name_is_new(self):
        sequencer = Sequencer()
        sequencer.begin()
        sequencer.add_name('TestBar')
        aged_names = list(sequencer.aged_names())
        assert len(aged_names) == 1
        assert aged_names[0].name == 'TestBar'
        assert aged_names[0].is_new is True

    def test_names_become_known(self):
        sequencer = Sequencer()
        sequencer.begin()
        sequencer.add_name('TestBar')
        unused = list(sequencer.aged_names())
        sequencer.begin()
        sequencer.add_name('TestFoo')
        aged_names = list(sequencer.aged_names())
        assert len(aged_names) == 2
        assert aged_names[0].name == 'TestBar'
        assert aged_names[0].is_new is False
        assert aged_names[1].name == 'TestFoo'
        assert aged_names[1].is_new is True

    def test_duplicates_do_not_occur(self):
        sequencer = Sequencer()
        sequencer.begin()
        sequencer.add_name('TestBar')
        sequencer.add_name('TestBar')
        aged_names = list(sequencer.aged_names())
        assert len(aged_names) == 1

    def test_begin_works_even_if_names_not_read_out(self):
        sequencer = Sequencer()
        sequencer.begin()
        sequencer.add_name('TestBar')
        sequencer.begin()
        sequencer.add_name('TestFoo')
        aged_names = list(sequencer.aged_names())
        assert len(aged_names) == 2
        assert aged_names[1].name == 'TestFoo'
        assert aged_names[1].is_new is True
        assert aged_names[0].name == 'TestBar'
        assert aged_names[0].is_new is False

    def test_add_name_provides_result(self):
        collator = Collator()
        collator.begin()
        collator.add(name='TestFoo', outcome='Fail')
        result = collator.result_for('TestFoo', True)
        assert result.name == 'TestFoo'
        assert result.outcome == 'Fail'
        assert result.is_new is True

    def test_missing_name_provides_unrun_result(self):
        collator = Collator()
        collator.begin()
        result = collator.result_for('TestBar', True)
        assert result.name == 'TestBar'
        assert result.outcome == 'Unrun'
        assert result.is_new is True

    def test_story_test(self):
        collator = Collator()
        collator.begin()
        collator.add(name='TestFoo', outcome='Pass')
        collator.add(name='TestBar', outcome='Fail')
        initial_result = list(collator.results())
        self.check(initial_result, 0,
                   'TestFoo', 'Pass', True)
        self.check(initial_result, 1,
                   'TestBar', 'Fail', True)
        collator.begin()
        collator.add(name='TestBaz', outcome='Pass')
        collator.add(name='TestBar', outcome='Pass')
        second_result = list(collator.results())
        self.check(second_result, 0,
                   'TestFoo', 'Unrun', False)
        self.check(second_result, 1,
                   'TestBar', 'Pass', False)
        self.check(second_result, 2,
                   'TestBaz', 'Pass', True)

    def check(self, results, index, name, outcome, new):
        result = results[index]
        assert result.name == name
        assert result.outcome == outcome
        assert result.is_new is new

    def test_with(self):
        collator = Collator()
        with collator:
            collator.add(name='TestFoo', outcome='Pass')
            collator.add(name='TestBar', outcome='Fail')
            initial_result = list(collator.results())
        with collator:
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
