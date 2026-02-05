import curses
from _curses import window

def main(stdscr: window) -> None:
    stdscr.clear()
    stdscr.addstr(0, 0, "This is a calculator:")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)