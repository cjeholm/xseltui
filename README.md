# xseltui
This is a small Python script that provides a curses TUI for clipboard management.

In the default state it depends on the package xsel for reading and settings the system clipboard. Also xclip can be used but it produces some errors when the clipboard is empty ie. after reboot.

xseltui does not save any history in any files, temporary or permanent.

#### Functions
- Automatically reads the system clipboard and puts new items in the buffer
- Allows for a selection of which buffer to push to the system clipboard
- Delete mode for removing buffer entries
- Truncating long entries in the list while showing total characters
