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
            # xclipHistory.append(xclipLatest)
            xclipHistory.insert(0, xclipLatest)

        if len(xclipHistory) > 9:
            xclipHistory.pop(-1)

        stdscr.clear()                  # clear screen
        stdscr.addstr(1, 5, clean(xclipLatest), curses.color_pair(7)) # Active clipboard

        lineNumber = 0
        while lineNumber < historyLength:
            if lineNumber == 0:
                stdscr.addstr(1 + lineNumber, 2, ">", curses.color_pair(3))
            else:
                stdscr.addstr(1 + lineNumber, 2, str(lineNumber), curses.color_pair(14))
            lineNumber += 1

        lineNumber = 1
        for item in xclipHistory:
            stdscr.addstr(1 + lineNumber, 5, clean(item), curses.color_pair(15))
            lineNumber += 1

        stdscr.addstr(12, 2, "(1-9) selects a buffer", curses.color_pair(14))
        stdscr.addstr(13, 2, "(x)   toggles Delete Mode", curses.color_pair(14))
        stdscr.addstr(14, 2, "(q)   quit", curses.color_pair(14))

        pressedKey = ''

        try:
            pressedKey = stdscr.getkey()
            stdscr.addstr(15, 2, pressedKey, curses.color_pair(2))
        except Exception:
            pass

        if pressedKey == 'q':
            exit()

        time.sleep(0.5)
        stdscr.refresh()


if __name__ == "__main__":
    # main()
    wrapper(main)
