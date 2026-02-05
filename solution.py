class Calculator():
    @staticmethod
    def calculate(*, expression: str) -> int | float:
        raise NotImplementedError
    
    @staticmethod
    def evaluate(*, operands: list[int], operators: list[str]) -> int:
        raise NotImplementedError