from status import Status


class TestCollated:
    def test_status(self):
        status = Status('TestFoo', 'Pass')
        assert status.name == 'TestFoo'
        assert status.outcome == 'Pass'