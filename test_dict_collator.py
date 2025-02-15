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

    def test_unrun(self):
        dc = DictCollator()
        with dc:
            dc.add('TestFoo', "Fail")
        with dc as collator:
            dc.add('TestBar', "Pass")
            results = dc.results()
        self.check(results,0, 'TestFoo', 'Unrun', False)
        self.check(results,1, 'TestBar', 'Pass', True)

    def test_three_phases(self):
        dc = DictCollator()
        with dc:
            dc.add('TestFoo', "Pass")
            dc.add('TestBar', "Pass")
            dc.add('TestBaz', "Fail")
            results = dc.results()
        assert [r.name for r in results] == ['TestFoo', 'TestBar', 'TestBaz']
        assert [r.outcome for r in results] == ['Pass', 'Pass', 'Fail']
        assert [r.is_new for r in results] == [True, True, True]

        with dc:
            dc.add('TestFoo', "Fail")
            dc.add('Test2New', 'Pass')
            results = dc.results()
        assert [r.name for r in results] == ['TestFoo', 'TestBar', 'TestBaz', 'Test2New']
        assert [r.outcome for r in results] == ['Fail', 'Unrun', 'Unrun', 'Pass']
        assert [r.is_new for r in results] == [False, False, False, True]

        with dc:
            dc.add('TestBar', 'Fail')
            dc.add('Test3New', 'Pass')
            results = dc.results()
        assert [r.name for r in results] == ['TestFoo', 'TestBar', 'TestBaz', 'Test2New', 'Test3New']
        assert [r.outcome for r in results] == ['Unrun', 'Fail', 'Unrun', 'Unrun', 'Pass']
        assert [r.is_new for r in results] == [False, False, False, False, True]

