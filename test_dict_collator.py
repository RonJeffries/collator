from dict_collator import DictCollator


class TestDictCollator:
    @staticmethod
    def check(results, index, name, outcome, new):
        result = results[index]
        assert result.name == name
        assert result.outcome == outcome
        assert result.is_new is new

    def test_exists(self):
        DictCollator()

    def test_context_manager(self):
        c = DictCollator()
        with c as d:
            pass

    def test_add_two_and_report(self):
        dc = DictCollator()
        with dc as collator:
            dc.add('TestFoo', "Pass")
            dc.add('TestBar', "Fail")
            results = dc.results()
            assert len(results) == 2
        self.check(results,
           0, 'TestFoo', 'Pass', True)
        self.check(results,
           1, 'TestBar', 'Fail', True)

    def test_old_and_new(self):
        dc = DictCollator()
        with dc as collator:
            dc.add('TestFoo', "Fail")
        with dc as collator:
            dc.add('TestBar', "Pass")
            dc.add('TestFoo', "Fail")
            results = dc.results()
        self.check(results,0, 'TestFoo', 'Fail', False)
        self.check(results,1, 'TestBar', 'Pass', True)
