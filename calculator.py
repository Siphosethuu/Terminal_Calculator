import re
from typing import Any


VALID_EXPRESSION_PATTERN: str = r"(([+-]*|\*{0,2}|/)?(\d+\.?|.?\d+|\d+\.?\d+))+"
class Calculator():
    @staticmethod
    def get_valid(expr: str, vars: dict[str, str] = None) -> Any:
        if vars is None:
            vars = {}

        for res in re.findall("[0-9.]preans", expr):
            expr = expr.replace(res, f"*{res}")
        for res in re.findall(r"preans[0-9.]", expr):
            expr = expr.replace(res, f"*{res}")

        expr = expr.replace(
            "preans", vars.get("preans", '0')
        )

        for var, value in vars:
            for res in re.findall(f"[0-9.]{var}", expr):
                expr = expr.replace(var, f"*{var}")
            for res in re.findall(f"{var}[0-9.]", expr):
                expr = expr.replace(var, f"{var}*")
            expr = expr.replace(var, f"{value}")

        if re.fullmatch(VALID_EXPRESSION_PATTERN, expr):
            return expr
