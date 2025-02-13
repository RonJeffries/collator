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