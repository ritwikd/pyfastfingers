import re
import sys
import curses
from time import time as get_time

WIN_WIDTH = 60
WIN_HEIGHT = 20
WIN_START_Y = 10
WIN_START_X = 10

WIN_TITLE_CENTER_POS = 23
WIN_TEXT_POS = 7
regex = re.compile('[\W_]+', re.UNICODE)


class FastFingers():

    def __init__(self, sentence):

        self.screen = curses.initscr()
        self.screen.keypad(1)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.window = curses.newwin(
            WIN_HEIGHT, WIN_WIDTH, WIN_START_Y, WIN_START_X)
        self.window.addstr(0, WIN_TITLE_CENTER_POS, 'PyFastFingers', curses.A_STANDOUT)
        self.window.refresh()
        self.screen.refresh()

        self.ff = FFWordList()
        self.ff.init_new_sentence(sentence)

        user_input_ascii = None
        program_started = False
        typing_done = False
        first_letter = True
        time_start = 0
        waiting_space = False
        program_done = False

        while not program_started:
            self.window.addstr(1, WIN_TITLE_CENTER_POS, 'PyFastFingers', curses.A_STANDOUT)
            self.window.addstr(
                4, WIN_TEXT_POS, 'Press any key to start.', curses.color_pair(3))
            self.window.box()
            self.window.refresh()
            user_input_ascii = self.screen.getch()
            if user_input_ascii > -1 and user_input_ascii < 256:
                if user_input_ascii == 32:
                    self.clear_screen()
                    program_started = True

        self.render_words()
        self.window.box()
        self.window.refresh()

        while not typing_done:
            user_input_ascii = self.screen.getch()
            if not waiting_space and user_input_ascii > -1 and user_input_ascii < 256:
                if first_letter:
                    time_start = get_time()
                    first_letter = False
                user_input_str = chr(user_input_ascii)
                user_input_new = self.ff.user_input + user_input_str
                user_input_check_result = self.ff.check_current_word(
                    user_input_new)
                color_pair = curses.color_pair(2)
                if user_input_check_result == 2:
                    if not self.ff.check_sentence_done():
                        waiting_space = True
                    else:
                        typing_done = self.ff.update_all_words()
                        self.window.refresh()
                        self.ff.update_user_input('')
                        self.window.addstr(4, 1, ' ' * (WIN_WIDTH - 2))
                        self.render_words()
                elif user_input_check_result == 1:
                    self.ff.update_user_input(user_input_new)
                else:
                    color_pair = curses.color_pair(1)
                user_input_padded = user_input_new + \
                    (' ' * (WIN_WIDTH - len(user_input_new) - 4))
                self.window.addstr(1, WIN_TITLE_CENTER_POS, 'PyFastFingers', curses.A_STANDOUT)
                self.window.addstr(10, WIN_TEXT_POS, user_input_padded, color_pair)
                self.render_words()
            if waiting_space:
                if user_input_ascii == 32:
                    typing_done = self.ff.update_all_words()
                    self.window.refresh()
                    waiting_space = False
                    self.ff.update_user_input('')
                    self.window.addstr(3, 2, ' ' * (WIN_WIDTH - 1))
                    self.render_words()

            self.window.box()
            self.window.refresh()

        time_end = get_time()
        ff_stats = self.ff.get_stats(time_start, time_end)

        self.clear_screen()
        self.window.refresh()

        while not program_done:
            self.window.addstr(1, WIN_TITLE_CENTER_POS, 'PyFastFingers', curses.A_STANDOUT)
            self.window.addstr(8, WIN_TEXT_POS, 'You typed at ' +
                               ff_stats[1] + ' WPM.', curses.A_BOLD)
            self.window.addstr(13, WIN_TEXT_POS, 'Press Q to quit.', curses.color_pair(3))
            self.window.box()
            self.window.refresh()
            user_input_ascii = self.screen.getch()
            self.window.addstr('')
            if user_input_ascii > -1 and user_input_ascii < 256:
                user_input_str = chr(user_input_ascii)
                if user_input_str == 'q' or user_input_str == 'Q':
                    self.close_screen()
                    program_done = True

    def render_words(self):
        render_output = self.ff.get_rest_of_sentence()
        current_word_to_render = render_output[0]
        rest_of_sentence = render_output[2]
        rest_of_sentence
        self.window.addstr(8, WIN_TEXT_POS, current_word_to_render, curses.A_STANDOUT)
        self.window.addstr(
            8, 5 + render_output[1], rest_of_sentence, curses.A_BOLD)

    def clear_screen(self):
        for i in xrange(1, WIN_HEIGHT):
            self.window.addstr(i, 1, ' ' * (WIN_WIDTH - 2))

    def close_screen(self):
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


class FFWordList():

    def __init__(self):
        self.sentence = ''
        self.words = []
        self.current_index = -1
        self.current_word = ''

        self.next_index = self.current_index + 1
        self.next_word = ''

        self.user_input = ''

    def update_user_input(self, user_input_new):
        self.user_input = user_input_new

    def get_user_input(self):
        return self.user_input

    def sentence_to_words(self):
        if self.sentence == '':
            return []
        else:
            return self.sentence.split(' ')

    def set_sentence(self, new_sentence):
        self.sentence = new_sentence
        self.words = self.sentence_to_words()

    def update_current_word(self):
        self.current_index += 1
        self.current_word = self.words[self.current_index]

    def update_next_word(self):
        self.next_index += 1
        self.next_word = self.words[self.next_index]

    def get_rest_of_sentence(self):
        word_to_return = self.current_word
        rest_to_return = ' ' + \
            ' '.join(self.words[(self.current_index + 1):]
                     )[:WIN_WIDTH - len(word_to_return) - 5]
        rest_to_return += ' ' * (WIN_WIDTH - len(rest_to_return) - 1)
        return [word_to_return, len(word_to_return), rest_to_return]

    def check_sentence_done(self):
        if self.current_index == len(self.words) - 1:
            return True
        return False

    def update_all_words(self):
        done = False
        if self.current_index < len(self.words) - 2:
            self.update_current_word()
            self.update_next_word()
        elif self.current_index < len(self.words) - 1:
            self.update_current_word()
            self.next_word = ''
        else:
            done = True
        return done

    def check_current_word(self, user_input):
        word_amt = len(user_input)
        if word_amt == len(self.current_word):
            if user_input == self.current_word:
                return 2
        elif user_input == self.current_word[:word_amt]:
            return 1
        return 0

    def init_new_sentence(self, new_sentence):
        self.set_sentence(new_sentence)
        self.current_index = -1
        self.next_index = 0
        self.update_all_words()

    def get_stats(self, time_start, time_end):
        time_elapsed = time_end - time_start
        sentence_length = len(self.sentence)
        time_min = float(time_elapsed) / 60.0
        chars_per_min = round(float(sentence_length) / time_min)
        words_per_min = round(float(chars_per_min) / 5.0)
        return map(lambda val: str(val), [chars_per_min, words_per_min])


def start_fast_fingers(type='sentence', ff_input_prog=[]):
    if type == 'words':
        return FastFingers(' '.join(map(lambda word_line: regex.sub('', word_line), ff_input_prog)))
    return FastFingers(ff_input_prog)

if __name__ == '__main__':
    cli_args = sys.argv
    ff_input_proc = None
    if len(cli_args) < 2:
        try: 
            print 'No input file specified. Falling back to interactive mode.'
            interactive_mode_type = raw_input('Sentence (s) or Word (w) entry mode: ')
            print interactive_mode_type
            if True in map(lambda kw: kw in interactive_mode_type, ['w', 'W']):
                ff_input_proc = []
                print 'Enter your words, one line at a time, and hit enter when you are done'
                user_input = raw_input('Enter word, or hit enter to finish: ')
                while user_input != '':
                    ff_input_proc.append(user_input)
                    user_input = raw_input('Enter word, or hit enter to finish: ')
                if len(ff_input_proc) == 0:
                    sys.exit('No words entered.')
                try:
                    PyFastFingers = FastFingers(
                        ' '.join(map(lambda word_line: regex.sub('', word_line), ff_input_proc)))
                except:
                    sys.exit('Error initializing PyFastFingers.')
            elif True in map(lambda kw: kw in interactive_mode_type, ['s', 'S']):
                ff_input_proc = raw_input('Enter your desired sentence. A-Z, 0-9 only:')
                ff_input_proc = ' '.join(map(lambda word: regex.sub('', word), ff_input_proc.split(' ')))
                try:
                    PyFastFingers = FastFingers(ff_input_proc)
                except:
                    sys.exit('Error initializing PyFastFingers.')
            else:
                sys.exit('No mode "' + interactive_mode_type + '" exists.')
        except:
            sys.exit('No arguments given.')
    ff_input_file = None
    try:
        input_file = open(sys.argv[1], 'r')
    except:
        sys.exit('Error reading input file.')
    ff_input_proc = input_file.readlines()
    PyFastFingers = None
    if len(input_ff) == 1:
        try:
            PyFastFingers = FastFingers(regex.sub('', ff_input_proc[0]))
        except:
            sys.exit('Error initializing PyFastFingers in sentence format.')
    else:
        try:
            PyFastFingers = FastFingers(
                ' '.join(map(lambda word_line: regex.sub('', word_line), ff_input_proc)))
        except:
            sys.exit('Error initializing PyFastFingers in word format.')