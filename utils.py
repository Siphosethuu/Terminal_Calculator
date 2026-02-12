import curses
from typing import Any
from os import get_terminal_size 




def select_choice(options: list[Any], center: bool = True) -> Any:

    """ 
        Function that allows a user to select a choice \
        given a list of options.
        Args:
            options: List of options, first char is title.
        Return:
            item selected by user.
    """

    current_selection: int = 0

    HEIGHT: int = len(options) + 3
    WIDTH: int = len(max(options, key=len)) + 3

    SYSTEM_WIDTH, SYSTEM_HEIGHT = get_terminal_size()

    curses.curs_set(0)
    begin_y: int = 0
    begin_x: int = 0
    if center:
        begin_y: int = ( SYSTEM_HEIGHT - HEIGHT) // 2
        begin_x: int = ( SYSTEM_WIDTH - WIDTH) // 2


    title: Any = options.pop(0)
    options_window: window = curses.newwin(
            HEIGHT, WIDTH,
            begin_y, begin_x
    )

    options_window.keypad(True)
    options_window.addstr(0, 0, f"{title}".center(WIDTH), curses.A_BOLD)


    while True:
        options_window.move(1, 1)
        options_window.clrtoeol()


        for index, option in enumerate(options):
            if index == current_selection:
                options_window.addstr(index + 1, 0, f"{option}".center(WIDTH), curses.A_STANDOUT | curses.COLOR_RED)
            else:
                options_window.addstr(index + 1, 0, f"{option}".center(WIDTH))

        key = options_window.getkey()

        match key:
            case "KEY_UP":
                current_selection -= 1
            case "KEY_DOWN":
                current_selection += 1
            case '\n':
                curses.curs_set(1)
                return options[current_selection]
        options_window.refresh()
        current_selection %= len(options)
