#!/usr/bin/env python3
import time
import os
import curses
from curses import wrapper

historyLength = 10

def main(stdscr):

    curses.use_default_colors()     # use terminal colors
    curses.curs_set(0)              # hide the cursor

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
        stdscr.addstr(1, 5, str(xclipLatest), curses.color_pair(7)) # Active clipboard

        lineNumber = 0
        while lineNumber < historyLength:
            if lineNumber == 0:
                stdscr.addstr(1 + lineNumber, 2, ">", curses.color_pair(3))
            else:
                stdscr.addstr(1 + lineNumber, 2, str(lineNumber), curses.color_pair(14))
            lineNumber += 1

        lineNumber = 1
        for item in xclipHistory:
            stdscr.addstr(1 + lineNumber, 5, str(item), curses.color_pair(15))
            lineNumber += 1

        stdscr.addstr(12, 2, "Keys (1-9) selects a buffer", curses.color_pair(14))
        stdscr.addstr(13, 2, "(x) toggles Delete Mode", curses.color_pair(14))

        stdscr.refresh()
        time.sleep(0.5)


if __name__ == "__main__":
    # main()
    wrapper(main)