import curses

WIN_WIDTH = 40
WIN_HEIGHT = 10
WIN_START_Y = 10
WIN_START_X = 10


class FastFingersScreen():

    def __init__(self):

        self.screen = curses.initscr()
        self.screen.keypad(1)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self.window = curses.newwin(
            WIN_HEIGHT, WIN_WIDTH, WIN_START_Y, WIN_START_X)

        self.screen.addstr(0, 0, "Starting PyFastFingers", curses.A_STANDOUT)
        self.screen.refresh()

        while 1:
            c = self.screen.getch()
            if c == ord('q') or c == ord('Q'):
                self.close_screen()
                break
            else:
                color_pair = curses.color_pair(1)
                if c > 100:
                    color_pair = curses.color_pair(2)
                self.screen.addstr(5,0,chr(c), color_pair)
                self.screen.refresh()

    def close_screen(self):
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


class FastFingersInternal():

    def __init__(self):
        self.sentence = ""
        self.words = []
        self.current_index = 0
        self.current_word = ""

    def sentence_to_words(self):
        if self.sentence == "":
            return []
        else:
            return self.sentence.split[" "]

    def set_sentence(self, new_sentence):
        self.sentence = new_sentence
        self.words = self.sentence_to_words(new_sentence)

    def update_current_word(self):
        self.current_word = self.words[self.current_index]

    def get_next_word(self):
        if self.current_index < len(self.words):
            self.current_index += 1
            self.update_current_word()
            return self.current_word
        else:
            return "FINISHED"

    def check_current_word(self, user_input):
        word_amt = len(user_input)
        if word_amt == len(self.current_word):
            if user_input == self.current_word:
                return 2
        if user_input == self.current_word[:word_amt]:
            return 1
        return 0

    def init_new_sentence(self, new_sentence):
        self.set_sentence(new_sentence)
        self.current_index = 0
        self.up
        date_current_word()

PyFastFingers = FastFingersScreen()
