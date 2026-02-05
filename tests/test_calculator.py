from main import calculate
class Test_Function():
    def test_basic(self) -> None:
        a: int = "1+1"
        assert calculate(number=a) == eval(a)
