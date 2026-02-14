import curses, sys, time, os
from _curses import window
from utils import OPERS, select_choice, take_input, SYSTEM_COLS


MENU: list[int] = [
    "Choose an activity:", # title
    "Calculator",
    "Little Prof",
    "View History",
    "View Help",
    "Quit"
]


def main(stdscr: window) -> None:
    global MENU
    stdscr.clear()
    stdscr.addstr(0, 0, "Calculator Program.".center(SYSTEM_COLS), curses.A_STANDOUT | curses.A_BOLD)
    try:
        user_choice: Any = select_choice(MENU)
    except curses.error as e:
        sys.exit(f"{e} (likely caused by terminal size being small...)")
    except Exception as e:
        sys.exit(f"{e}")

    match user_choice:
        case "Calculator":
            sys.exit()
        case "Little Prof":
            sys.exit()
        case "View History":
            sys.exit()
        case "Quit":
            sys.exit()
    stdscr.refresh()



def calculate(win: window) -> None:
    global OPERS
    is_valid: "function" = lambda key: key.isdigit() \
            or key in OPERS

    prompt: str = "= "
    lock: threading.Lock = threading.Lock()
    user_input: list[str] = []
    take_input(win, 
        prompt=prompt, lock=lock,
        user_input=user_input, is_valid=is_valid
    )
    while True:
        lock.acquire()
        print
        lock.release()

curses.wrapper(main)
