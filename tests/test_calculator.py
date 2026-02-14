from calculator import Calculator as calc 
import pytest


class Test_Function():
    def test_basic(self) -> None:
        a: str = "1+1"
        assert calc.get_valid(a) == a

    def test_single_value(self) -> None:
        a: str = "10"
        assert calc.get_valid(a) == a

    @pytest.mark.parametrize("inp", ["+-+-10", "**3", "-5", "---100"])
    def test_single_with_signs(self, inp) -> None:
        assert calc.get_valid(inp) == inp

    
    @pytest.mark.parametrize("inp",
        ["+-7-76", "5**7", "98/0", "sioho"])
    def test_full_expressions(self, inp) -> None:
        assert calc.get_valid(inp) == inp




