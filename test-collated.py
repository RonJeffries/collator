from aged_name import AgedName
from collator import Collator
from result import Result
from status import Status


class TestCollated:
    def test_status(self):
        status = Status('TestFoo', 'Pass')
        assert status.name == 'TestFoo'
        assert status.outcome == 'Pass'

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
        collator = Collator()
        collator.begin()
        collator.add_name('TestBar')
        aged_names = list(collator.aged_names())
        assert len(aged_names) == 1
        assert aged_names[0].name == 'TestBar'
        assert aged_names[0].is_new is True

    def test_names_become_known(self):
        collator = Collator()
        collator.begin()
        collator.add_name('TestBar')
        unused = list(collator.aged_names())
        collator.begin()
        collator.add_name('TestFoo')
        aged_names = list(collator.aged_names())
        assert len(aged_names) == 2
        assert aged_names[0].name == 'TestBar'
        assert aged_names[0].is_new is False
        assert aged_names[1].name == 'TestFoo'
        assert aged_names[1].is_new is True

    def test_duplicates_do_not_occur(self):
        collator = Collator()
        collator.begin()
        collator.add_name('TestBar')
        collator.add_name('TestBar')
        aged_names = list(collator.aged_names())
        assert len(aged_names) == 1

    def test_begin_works_even_if_names_not_read_out(self):
        collator = Collator()
        collator.begin()
        collator.add_name('TestBar')
        collator.begin()
        collator.add_name('TestFoo')
        aged_names = list(collator.aged_names())
        assert len(aged_names) == 2
        assert aged_names[1].name == 'TestFoo'
        assert aged_names[1].is_new is True
        assert aged_names[0].name == 'TestBar'
        assert aged_names[0].is_new is False