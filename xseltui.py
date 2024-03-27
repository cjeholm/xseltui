#!/usr/bin/env python3

# xseltui by Conny Holm 2024
# TUI clipboard manager for x using xsel or xclip

import time
import os
import curses
from curses import wrapper

historyLength = 10

readClipboard = 'xsel -ob'
setClipboard = 'xsel -ib'


# Truncate and remove linebreaks from list items
def clean(cols, input):
    # maxLength = 40
    if cols < 22:
        maxLength = 10
    else:
        maxLength = cols - 18
    if len(input) > maxLength:
        input = str(input[:maxLength]) + f" ... [{len(input)}]"
    output = input.strip().replace("\n", "\\")
    return output


# The main function
def main(stdscr):

    curses.use_default_colors()     # use terminal colors
    curses.curs_set(0)              # hide the cursor
    stdscr.nodelay(1)               # Don't wait for keypress to loop. Redraws windows when resized.
    stdscr.keypad(1)                # Something with keypress idk

    deleteMode = False

    # Set colors
    i = 0
    while i < 16:
        curses.init_pair(i, i, -1)
        i += 1

    xclipHistory = []
    print(xclipHistory)

    # Main l00p
    while True:
        try:
            xclipLatest = os.popen(readClipboard).read()
            if xclipLatest in xclipHistory:
                pass
            else:
                # Insert latest at the beginning on list
                xclipHistory.insert(0, xclipLatest)
        except Exception:
            pass
        
        # Get rows and cols for linebreaking
        rows, cols = stdscr.getmaxyx()
        
        # Maintain max length of list
        if len(xclipHistory) > 9:
            xclipHistory.pop(-1)

        stdscr.erase()                  # clear screen
        stdscr.addstr(1, 5, clean(cols, xclipLatest), curses.color_pair(3))  # Active clipboard

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
            stdscr.addstr(1 + lineNumber, 5, clean(cols, item), curses.color_pair(15))
            lineNumber += 1

        # Write info text at the bottom
        if deleteMode is False:
            stdscr.addstr(12, 2, "(1-9) set system clipboard", curses.color_pair(14))
            stdscr.addstr(13, 2, "(x)   toggle Delete Mode", curses.color_pair(14))
            stdscr.addstr(14, 2, "(q)   quit", curses.color_pair(14))

        if deleteMode is True:
            stdscr.addstr(12, 2, "(1-9) select a buffer to delete", curses.color_pair(1))
            stdscr.addstr(13, 2, "(x)   cancel Delete Mode", curses.color_pair(14))

        # Keypress fetching
        pressedKey = ''

        try:
            pressedKey = stdscr.getkey()
            # stdscr.addstr(15, 2, pressedKey, curses.color_pair(1))
            if int(pressedKey) <= 9 and int(pressedKey) >= 1:
                if deleteMode is True:
                    xclipHistory.pop(int(pressedKey) - 1)
                    deleteMode = False
                else:
                    os.popen(f'echo -n "{xclipHistory[int(pressedKey) - 1]}" | {setClipboard}')
        except Exception:
            pass

        if pressedKey == 'x':
            if deleteMode is False:
                deleteMode = True
            else:
                deleteMode = False

        if pressedKey == 'q':
            exit()

        # Sleep and loop
        time.sleep(0.1)
        stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
