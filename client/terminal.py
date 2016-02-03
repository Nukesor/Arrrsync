import curses

from client.interpreter import Interpreter


class Terminal():
    def __init__(self, client, rsync):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(2)
        self.screen.keypad(True)
        self.screen.refresh()

        self.get_dimensions()

        self.history = []
        self.historyIndex = 0
        self.lines = []
        self.buffer = ''
        self.prompt = '>>: '

        self.client = client
        self.rsync = rsync
        self.interpreter = Interpreter(client, rsync, self)
        self.draw()

    def draw(self):
        row = 0
        self.screen.clear()
        topbuffer = 1
        leftbuffer = 1
        lineCount = len(self.lines)
        if lineCount < self.rows - 5:
            for line in self.lines:
                self.screen.addstr(row + topbuffer, leftbuffer, line)
                row += 1
        else:
            for index in range(lineCount-self.rows+5, lineCount-1):
                self.screen.addstr(row + topbuffer, leftbuffer, self.lines[index])
                row += 1

        self.screen.addstr(row + topbuffer, leftbuffer, self.prompt + self.buffer)

    def update(self):
        try:
            key = self.screen.getkey()
        except KeyboardInterrupt:
            # CTRL-C jumps to a blank input
            self.lines.append(self.prompt + self.buffer)
            self.buffer = ''
            self.draw()
            return True
        except:
            return True

        # Key up or left to up the history
        if key == 'KEY_UP' or key == 'KEY_LEFT':
            self.historyIndex -= 1
            if self.historyIndex < 0:
                self.historyIndex = 0
            if self.historyIndex <= len(self.history)-1:
                self.buffer = str(self.history[self.historyIndex])

        # Key down or right to go down the history
        elif key == 'KEY_DOWN' or key == 'KEY_RIGHT':
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
            self.lines.append(self.prompt + self.buffer)
            self.history.append(self.buffer)
            self.historyIndex = len(self.history)
            if not self.interpreter.interpret(self.buffer):
                return False
            self.buffer = ''

        # Remove stuff from current buffer
        elif key == 'KEY_BACKSPACE':
            self.buffer = self.buffer[:-1]

        # Tab for completion
        elif key == '\t':
            1+1

        # Screen clearing
        elif key == '\f':
            1+1

        # Trigger redraw for terminal resize
        elif key == 'KEY_RESIZE':
            self.buffer += key
            self.draw()

        # New char to command
        elif not key == 'KEY_RESIZE':
            self.buffer += key

        self.draw()

        return True

    def add_lines(self, lines):
        self.lines += lines

    def add_line(self, line):
        self.lines.append(line)

    def restore_terminal(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def get_dimensions(self):
        self.colums = curses.COLS
        self.rows = curses.LINES
