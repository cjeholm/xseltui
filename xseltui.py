#!/usr/bin/env python3

# xseltui by Conny Holm 2024
# TUI clipboard manager for x using xsel or xclip

import time
import sys
import os
import curses
from curses import wrapper

HISTORY_LENGTH = 10

READ_CLIPBOARD = 'xsel -ob'
SET_CLIPBOARD = 'xsel -ib'


# Truncate and remove linebreaks from list items
def clean(cols, list_item):
    # maxLength = 40
    if cols < 22:
        max_length = 10
    else:
        max_length = cols - 18
    if len(list_item) > max_length:
        list_item = str(list_item[:max_length]) + f" ... [{len(list_item)}]"

    return list_item.strip().replace("\n", "\\")


# The main function
def main(stdscr):

    curses.use_default_colors()     # use terminal colors
    curses.curs_set(0)              # hide the cursor
    stdscr.nodelay(1)               # Don't wait for keypress to loop. Redraws windows when resized.
    stdscr.keypad(1)                # Something with keypress idk

    delete_mode = False

    # Set colors
    i = 0
    while i < 16:
        curses.init_pair(i, i, -1)
        i += 1

    xsel_history = []

    # Main l00p
    while True:
        try:
            xsel_latest = os.popen(READ_CLIPBOARD).read()
            if xsel_latest in xsel_history:
                pass
            else:
                # Insert latest at the beginning on list
                xsel_history.insert(0, xsel_latest)
        except Exception:
            pass

        # Get rows and cols for linebreaking
        rows, cols = stdscr.getmaxyx()

        # Maintain max length of list
        if len(xsel_history) > 9:
            xsel_history.pop(-1)

        stdscr.erase()                  # clear screen
        stdscr.addstr(1, 5, clean(cols, xsel_latest), curses.color_pair(3))  # Active clipboard

        # Write line numbers
        line_number = 0
        while line_number < HISTORY_LENGTH:
            if line_number == 0:
                stdscr.addstr(1 + line_number, 2, ">", curses.color_pair(3))
            else:
                stdscr.addstr(1 + line_number, 2, str(line_number), curses.color_pair(14))
            line_number += 1

        # Write the history list
        line_number = 1
        for item in xsel_history:
            stdscr.addstr(1 + line_number, 5, clean(cols, item), curses.color_pair(15))
            line_number += 1

        # Write info text at the bottom
        if delete_mode is False:
            stdscr.addstr(12, 2, "(1-9) set system clipboard", curses.color_pair(14))
            stdscr.addstr(13, 2, "(x)   toggle Delete Mode", curses.color_pair(14))
            stdscr.addstr(14, 2, "(q)   quit", curses.color_pair(14))

        if delete_mode is True:
            stdscr.addstr(12, 2, "(1-9) select a buffer to delete", curses.color_pair(1))
            stdscr.addstr(13, 2, "(x)   cancel Delete Mode", curses.color_pair(14))

        # Keypress fetching
        pressed_key = ''

        try:
            pressed_key = stdscr.getkey()
            # stdscr.addstr(15, 2, pressedKey, curses.color_pair(1))
            if int(pressed_key) <= 9 and int(pressed_key) >= 1:
                if delete_mode is True:
                    xsel_history.pop(int(pressed_key) - 1)
                    delete_mode = False
                else:
                    to_clipboard = xsel_history[int(pressed_key) - 1]
                    to_clipboard = to_clipboard.replace("`", "\`")
                    os.popen(f'echo -n "{to_clipboard}" | {SET_CLIPBOARD}')
        except Exception:
            pass

        if pressed_key == 'x':
            delete_mode = not delete_mode

        if pressed_key == 'q':
            sys.exit()

        # Sleep and loop
        time.sleep(0.1)
        stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
