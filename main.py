import curses, sys
from _curses import window
from utils import select_choice


MENU: list[int] = [
        "Choose an activity:", # title
        "Calculator",
        "Little Prof",
        "View History",
        "Exit"
]


def main(stdscr: window) -> None:
    global MENU
    stdscr.clear()
    stdscr.addstr(0, 0, "This is a calculator:")
    try:
        user_choice: Any = select_choice(MENU)
    except curses.error as e:
        sys.exit(f"{e} (likely caused by terminal size being small...)")
    except Exception as e:
        sys.exit(f"{e}")

    stdscr.addstr(f"\n{user_choice = }")
    stdscr.refresh()
    stdscr.getch()


curses.wrapper(main)
