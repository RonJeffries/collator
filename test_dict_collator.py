from dict_collator import DictCollator


class TestDictCollator:
    def test_exists(self):
        DictCollator()

    def test_context_manager(self):
        c = DictCollator()
        with c as d:
            pass