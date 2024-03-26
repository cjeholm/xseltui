#!/usr/bin/env python3
import time
import os
import curses
from curses import wrapper

historyLength = 10

def main(stdscr):

    curses.use_default_colors()     # use terminal colors
    curses.curs_set(0)              # hide the cursor
    curses.init_pair(1, 14, -1)     # color pair 1: color no 14 and transparent background
    curses.init_pair(2, 3, -1)      # color pair 2: color no 7
    curses.init_pair(3, 15, -1)
    curses.init_pair(4, 7, -1)

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
        stdscr.addstr(1, 5, str(xclipLatest), curses.color_pair(4)) # Active clipboard

        lineNumber = 0
        while lineNumber < historyLength:
            if lineNumber == 0:
                stdscr.addstr(1 + lineNumber, 2, ">", curses.color_pair(2))
            else:
                stdscr.addstr(1 + lineNumber, 2, str(lineNumber), curses.color_pair(1))
            lineNumber += 1

        lineNumber = 1
        for item in xclipHistory:
            stdscr.addstr(1 + lineNumber, 5, str(item), curses.color_pair(3))
            lineNumber += 1

        stdscr.addstr(12, 2, "Keys (1-9) selects a buffer", curses.color_pair(1))
        stdscr.addstr(13, 2, "(x) toggles Delete Mode", curses.color_pair(1))

        stdscr.refresh()
        time.sleep(0.5)


if __name__ == "__main__":
    # main()
    wrapper(main)
