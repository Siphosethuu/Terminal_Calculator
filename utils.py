import curses, string
from typing import Any
from os import get_terminal_size 
from _curses import window
from threading import Lock

size = get_terminal_size()
SYSTEM_ROWS: int = size.lines
SYSTEM_COLS: int = size.columns
OTHER_DEFAULT: str = string.punctuation + " "

OPERS: tuple[str] = (
    '+', '-', '/', '*', '(', ')', '!',
)



def select_choice(options: list[Any], center: bool = True) -> Any:

    """ 
        Prompts a user to select a choice \
        given a list of options.
        Args:
            options: List of options, first item is title.
            center: bool, set to True by default, centers the prompt.
        Raises:
            ValueError: If the options are less than 2
            TypeError: If the options are not a list.
            curses.error: Id something occurs
        Returns:
            Any: The item selected by user.
    """
    if len(options) < 2:
        raise ValueError(
            "The are no options to choose from."
        )
    if not isinstance(options, list):
        raise TypeError(
            "The options must be a list."
        )

    current_selection: int = 0

    HEIGHT: int = len(options) + 3
    WIDTH: int = len(max(options, key=len)) + 3

    curses.curs_set(0)
    begin_y: int = 0
    begin_x: int = 0
    if center:
        begin_y: int = ( SYSTEM_ROWS - HEIGHT) // 2
        begin_x: int = ( SYSTEM_COLS - WIDTH) // 2


    title: Any = options.pop(0)
    options_window: window = curses.newwin(
            HEIGHT, WIDTH,
            begin_y, begin_x
    )

    options_window.keypad(True)
    options_window.addstr(0, 0, f"{title}".center(WIDTH), curses.A_BOLD)


    while True:
        #options_window.move(1, 1)
        #options_window.clrtoeol()

        for index, option in enumerate(options):
            start_x: int = (WIDTH - len(option)) // 2
            if index == current_selection:
                options_window.addstr(
                    index + 1, start_x, f"{option}",
                    curses.A_REVERSE | curses.A_STANDOUT)
        
            else:
                options_window.addstr(
                    index + 1, start_x, f"{option}"
                )

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



def take_input(win: window, **kwargs) -> list[str]:
    """
        Takes input from user until user clicks enter.
        Args:
            win: A window to put the input taker.
            kwargs:
                prompt: The user's prompt
                user_input: list of chars, can be used to process input as is type
                lock: A lock, should be passed if user_input is used concurrently in another program
                is_valid: A function that defines valid input characters.
                
        Returns:
            list: char typed by the user

    """
    global SYSTEM_COLS, OTHER_DEFAULT

    user_input: list[str] = kwargs.get("user_input", [])
    is_valid: "function" = kwargs.get("is_valid",
        lambda key: str.isalnum(key) or key in OTHER_DEFAULT
    )
    prompt: str = kwargs.get("prompt", '')

    lock: Lock = kwargs.get("lock", None)

    cursor_y, cursor_x = win.getyx()
    if cursor_x != 0:
        cursor_y += 1
    win.addstr(cursor_y, 0, prompt)
    cursor_x = len(prompt)


    index: int = len(user_input)
    curses.curs_set(1)

    def end_of_input() -> int:
        """
            Helper function that just calculates the last line convered by input.
        """
        this: int = cursor_x + len(user_input)
        return cursor_y + (this // SYSTEM_COLS)

    while True:
        win.move(cursor_y, cursor_x)
        _clr_win_until(win, end_of_input())
        win.addstr(cursor_y, cursor_x, ''.join(user_input))
        win.move(
            cursor_y + ((cursor_x + index) // SYSTEM_COLS),
            (cursor_x + index ) % SYSTEM_COLS
        )
        key = win.getkey()
        if lock:
            lock.acquire()
        match key:
            case "KEY_LEFT":
                index = (index - 1) % len(user_input) if user_input else 0
            case "KEY_RIGHT":
                index = (index + 1) % (len(user_input) + 1)
            case "KEY_UP":
                if cursor_x + index < SYSTEM_COLS:
                    continue
                index = max(index - SYSTEM_COLS, 0)
            case "KEY_DOWN":
                size_: int = len(user_input)
                if (cursor_x + index) - SYSTEM_COLS >= SYSTEM_COLS:
                    continue
                index = min(
                    index + SYSTEM_COLS,
                    size_
                )
            case "KEY_BACKSPACE" | '\b' | '\x7f':
                if not user_input: continue
                index -= 1
                user_input.pop(index)
            case '=' | '\n':
                return user_input
            case _:
                if not is_valid(key):
                    continue
                user_input.insert(index, key)
                index += 1
        if lock:
            lock.release() 
        win.refresh()


 
def _clr_win_until(win: window, line: int) -> None:
    """
        Clears the given window from the windows current cursor position until the end of the line specified by user.
        Args:
            win: The window to clear.
            line: The number of the line to clear until
        Raises:
            exception: I don't know yet.
        
    """
    current_y, current_x = win.getyx()
    for step in range(current_y, line + 1):
        win.clrtoeol()
        win.move(current_y + step, 0)
