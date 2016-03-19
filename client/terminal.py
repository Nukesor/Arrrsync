import math
import curses

from client.interpreter import Interpreter
from client.completer import Completer


class Terminal():
    def __init__(self, client, rsync):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(2)
        self.screen.keypad(True)
        self.screen.refresh()

        self.get_dimensions()

        self.lines = []
        self.displayedLines = 0
        self.viewport = 0

        self.history = []
        self.historyIndex = 0

        self.buffer = ''
        self.prompt = '>>: '
        self.completionActive = False

        self.client = client
        self.rsync = rsync
        self.interpreter = Interpreter(client, rsync, self)
        self.completer = Completer(client, self)
        self.draw()

    def draw(self):
        # Runner for lines
        row = 0
        start = 0
        end = 0
        # Get the amount of already added lines in history
        lineCount = len(self.lines)

        # Buffer variables
        topbuffer = 1
        bottombuffer = 2
        leftbuffer = 1

        # Screen clearing for redrawing
        self.screen.clear()

        # Calculate end and start indices of self.lines for drawing
        if lineCount < self.rows - bottombuffer:
            start = 0
            end = lineCount
        else:
            if self.viewport > (lineCount - self.rows + bottombuffer):
                self.viewport = (lineCount - self.rows + bottombuffer)
            elif self.viewport < 0:
                self.viewport = 0
            start = lineCount - self.rows + bottombuffer - self.viewport
            end = lineCount - self.viewport

        # Draw the lines in specified range
        for index in range(start, end):
            self.screen.addstr(row + topbuffer, leftbuffer, self.lines[index])
            row += 1

        # Drawing of the current buffer ( userinput )
        self.screen.addstr(self.rows-1, leftbuffer, self.prompt + self.buffer)

    def update(self):
        try:
            key = self.screen.getkey()
        except KeyboardInterrupt:
            # CTRL-C jumps to a blank input
            self.lines.append(self.prompt + self.buffer)
            self.buffer = ''
            self.draw()
            self.completionActive = False
            return True
        except:
            return True

        # Key up or left to up the history
        if key == 'KEY_UP' or key == 'KEY_LEFT':
            self.completionActive = False
            self.historyIndex -= 1
            if self.historyIndex < 0:
                self.historyIndex = 0
            if self.historyIndex <= len(self.history)-1:
                self.buffer = str(self.history[self.historyIndex])

        # Key down or right to go down the history
        elif key == 'KEY_DOWN' or key == 'KEY_RIGHT':
            self.completionActive = False
            self.historyIndex += 1
            if self.historyIndex > len(self.history) - 1:
                self.historyIndex = len(self.history)
                self.buffer = ''
            elif self.history[self.historyIndex]:
                self.buffer = str(self.history[self.historyIndex])

        # CTLR-D exits the program
        elif key == '^D':
            return False

        # Newline returns command
        elif key == '\n':
            self.completionActive = False
            try:
                # Call interpreter on current buffer
                if not self.interpreter.interpret(self.buffer):
                    return False
            except KeyboardInterrupt:
                # The current command is being interrupted with ctrl+c.
                # Proceed like a normal ^C
                pass
            # Add command to draw buffer
            self.add_line(self.prompt + self.buffer)
            # Append command to history and reset historyIndex
            self.history.append(self.buffer)
            self.historyIndex = len(self.history)
            # Clear buffer and reset viewport
            self.buffer = ''
            self.viewport = 0

        # Remove stuff from current buffer
        elif key == 'KEY_BACKSPACE':
            self.completionActive = False
            self.buffer = self.buffer[:-1]

        # Tab for completion
        elif key == '\t':
            try:
                if not self.completionActive:
                    self.buffer = self.completer.complete(self.buffer)
                else:
                    self.buffer = self.completer.next()
                self.completionActive = True
            except KeyboardInterrupt:
                pass

        # Scroll history down
        elif key == 'KEY_PPAGE':
            self.viewport += math.floor(self.rows/2)

        # Scroll history up
        elif key == 'KEY_NPAGE':
            self.viewport -= math.floor(self.rows/2)

        # Screen clearing
        elif key == '\f':
            self.lines = []
            self.viewport = 0

        # Trigger redraw for terminal resize
        elif key == 'KEY_RESIZE':
            self.buffer += key
            self.get_dimensions()
            self.draw()

        # New char to command
        else:
            self.completionActive = False
            self.buffer += key

        self.draw()
        return True

    def add_lines(self, lines):
        self.lines += lines
        self.displayedLines += len(lines)

    def add_line(self, line):
        self.lines.append(line)
        self.displayedLines += 1

    def restore_terminal(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def get_dimensions(self):
        self.rows, self.columns = self.screen.getmaxyx()

    def update_last_lines(self, lines):
        for index, line in enumerate(lines):
            new_index = len(self.lines)-1-len(lines)+index
            self.lines[new_index] = line
        self.draw()
