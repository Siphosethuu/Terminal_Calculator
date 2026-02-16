import re
from typing import Any
from threading import Lock


NUM_PATTERN: str = r"([+-]{2,}(?:\d+\.|\.\d+|\d+\.\d+|\d+))"


class Calculator():
    def __init__(self, lock: Lock = None) -> None:
        self.preans: int = 0
        self.ans: int = 0
        self.lock = lock


    def get_valid(self, num: str) -> str:
        if not num:
            raise ValueError(
                "Num is invalid."
            )
        num: str = num.replace('+', '')
        return num.replace("--", '')


    def calculate(self, expression: list[str]) -> Any:
        if self.lock:
            self.lock.acquire()
        expr = ''.join(expression)
        for var in ("preans", "ans"):
            for c in re.findall(f"[0-9]{var}", expr):
                expr = expr.replace(c, f"{c[0]}*{var}")
            for c in re.findall(f"{var}[0-9]", expr):
                expr = expr.replace(c, f"{var}*{c[-1]}")
            expr = expr.replace(var,
                f"{getattr(self, var)}"
            )
        for c in re.findall(r"[0-9]\(", expr):
            expr = expr.replace(c, f"{c[0]}*(")

        for c in re.findall(r"\)[0-9]", expr):
            expr = expr.replace(c, f")*{c[-1]}")

        for match in re.findall(NUM_PATTERN, expr):
            expr = expr.replace(match, self.get_valid(match))

        try:
            return eval(expr), "Successful"

        except ZeroDivisionError as e:
            return None, "ComplexInfinity"
        except Exception as e:
            return None, ""

        finally:
            if self.lock:
                self.lock.release()

if __name__ == "__main__":
    calc: Calculator = Calculator()
    expr: str = "+-+67**2-7(78)"
    print(expr)
    print(calc.calculate(list(expr)))

