#!/usr/bin/env python3
import time
import os
import curses
from curses import wrapper

historyLength = 10


# Truncate and remove linebreaks from list items
def clean(input):
    maxLength = 40
    if len(input) > maxLength:
        input = str(input[:maxLength]) + f" ... [{len(input)}]"
    output = input.strip().replace("\n", "\\")
    return output


def main(stdscr):

    curses.use_default_colors()     # use terminal colors
    curses.curs_set(0)              # hide the cursor
    stdscr.nodelay(1)
    stdscr.keypad(1)

    # Set colors
    i = 0
    while i < 16:
        curses.init_pair(i, i, -1)
        i += 1

    xclipHistory = []
    print(xclipHistory)

    while True:
        xclipLatest = os.popen('xclip -o -sel c').read()
        if xclipLatest in xclipHistory:
            pass
        else:
            # Insert latest at the beginning on list
            xclipHistory.insert(0, xclipLatest)

        # Maintain max length of list
        if len(xclipHistory) > 9:
            xclipHistory.pop(-1)

        stdscr.clear()                  # clear screen
        stdscr.addstr(1, 5, clean(xclipLatest), curses.color_pair(7)) # Active clipboard

        # Write line numbers
        lineNumber = 0
        while lineNumber < historyLength:
            if lineNumber == 0:
                stdscr.addstr(1 + lineNumber, 2, ">", curses.color_pair(3))
            else:
                stdscr.addstr(1 + lineNumber, 2, str(lineNumber), curses.color_pair(14))
            lineNumber += 1

        # Write the history list
        lineNumber = 1
        for item in xclipHistory:
            stdscr.addstr(1 + lineNumber, 5, clean(item), curses.color_pair(15))
            lineNumber += 1

        # Write info text at the bottom
        stdscr.addstr(12, 2, "(1-9) selects a buffer", curses.color_pair(14))
        stdscr.addstr(13, 2, "(x)   toggles Delete Mode", curses.color_pair(14))
        stdscr.addstr(14, 2, "(q)   quit", curses.color_pair(14))

        # Keypress fetching
        pressedKey = ''

        try:
            pressedKey = stdscr.getkey()
            # stdscr.addstr(15, 2, pressedKey, curses.color_pair(1))
            if int(pressedKey) <= 9 and int(pressedKey) >= 1:
                os.popen(f'echo -n "{xclipHistory[int(pressedKey) - 1]}" | xclip -i -selection clipboard')
        except Exception:
            pass

        if pressedKey == 'q':
            exit()

        time.sleep(0.1)
        stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
