class Little_Professor:
    def __init__(self) -> None:
        self._round: int = 1
        self.__session_high: int = 1


    @property
    def round(self) -> int:
        return self._round

    def generate_expression(self) -> str:
        raise NotImplementedError
    
    def play_game(self) -> None:
        raise NotImplementedError

    def update_score(self) -> None:
        while True:
            self.__session_high = max(
                self.__session_high, self.round
            )

