'''
Created on 30 Jan. 2012
Finished on 6 Feb. 2012

Improvements:
 - 31 Mar. 2020 to 31 Mar. 2020: fixed compatibility issues of Matplotlib and Tinker on OS X machines.
 - 19 Nov. 2019 to 22 Nov. 2019: rewrote Programming for Economists ipy_lib to Python 3.7 and merged with this one.
 - 15 Nov. 2019 to 18 Nov. 2019: rewrote ipy_lib to Python 3.7 and fixed compatibility issues.
 - 1 Mar. 2012 to 2 Mar. 2012: fixed a rare threading related crash
 - 3 Mar. 2012 to 5 Mar. 2012: fixed a bug in showing names of the barchart
 - 17 Mar. 2012 to 18 Mar. 2012: fixed not running on Linux
 - 31 Jul. 2012 to 31 Jul. 2012: added UserInput and 'privatised' most classes and imports
 - 1 Aug. 2012 to 2 Aug. 2012: fixed another bug with showing names of the barchart and a bug with displaying text in othello
 - 4 Aug. 2012 to 4 Aug. 2012: fixed bug with opening a file and fixed functionality of closing the window
 - 6 Aug. 2012 to 7 Aug. 2012: fixed multiple windows crashing the UI, reverted change to UserInput with this change
 - 21 Aug. 2012 to 21 Aug. 2012: adjusted naming from JAVA to Python convention, changed UserInput to a function that returns all input, added Life interface
 - 22 Aug. 2012 to 22 Aug. 2012: added scrollbar to othello, snake and life interfaces, added type checking and exceptions for all input
 - 2 Sep. 2012 to 2 Sep. 2012: fixed another bug with names of the barchart, allowed ints to be given to floats, fixed spelling
 - 13 Sep. 2012 to 13 Sep. 2012: fixed more spelling, added functionality for multiple answers per question
 - 27 Sep. 2012 to 27 Sep. 2012: changed multiple answers from array to arbitrary arguments list, added exception if argument list is empty
 - 6 Dec. 2012 to 6. Dec. 2012: fixed resets of auto alarm speed by adding a timer
 - 2 Oct. 2013 to 3. Oct. 2013: fixed ranged errors, fixed closing bug in Windows and Linux when only calling ask_user or file_input,
                                fixed typos, added Escape as window closer, fixed window not getting focus when started, added Mac support (!)
 - 9 Oct. 2013 to 9. Oct. 2013: fixed get_event (Mac version) to properly give refresh events
 - 12 Nov. 2014 to 12. Nov. 2014: fixed OS X to not use PIL anymore and instead of images draw some simple shapes
 - 21 Nov. 2014 to 21. Nov. 2014: fixed OS X BarChartUI to properly show bar names without calling show
 - 15 May. 2015 to 15 May. 2015: added user interfaces for programming for economy -- Sebastian
 - 22 Jun. 2015 to 22 Jun. 2015: fixed asking twice for file_input on Windows -- Gerben

@author: Gerben Rozie
@author: Sebastian Osterlund
@author: Sander Benoist
'''
import tkinter as _tk
import tkinter.dialog as _Dialog
import tkinter.filedialog as _tkFileDialog
import tkinter.messagebox as _tkMessageBox
import queue as _Queue
import time as _time
import os as _os
import random as _random
import sys as _sys

class _IPyException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def _verify_int(value_var, string_var, minimum=None, maximum=None):
    if not isinstance(value_var, int):
        value = "%s not an int for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)
    _verify_input(value_var, string_var, minimum, maximum)


def _verify_float(value_var, string_var, minimum=None, maximum=None):
    if not isinstance(value_var, float):
        if not isinstance(value_var, int):
            value = "%s is not a float or int for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
            raise _IPyException(value)
    _verify_input(value_var, string_var, minimum, maximum)


def _verify_str(value_var, string_var):
    if not isinstance(value_var, str):
        value = "%s is not a string for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)


def _verify_bool(value_var, string_var):
    if not isinstance(value_var, bool):
        value = "%s is not a boolean for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)


def _verify_input(value_var, string_var, minimum=None, maximum=None):
    if minimum is None:
        minimum = float('-inf')
    if maximum is None:
        maximum = float('inf')
    if value_var >= minimum:
        if value_var <= maximum:
            return
    value = "%s is out of bounds, expected range: %s to %s, got: %s" % (string_var, minimum, maximum, value_var)
    raise _IPyException(value)





class _LifeHolder(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    _ui_factory = None


def file_input():
    """This function lets the user select a file to use for input.
	Returns the file contents in a string.
	"""

    global _ui_factory
    f = _AskInput(_ui_factory.mainroot).f
    if f == '':
        return None
    return str(_sys.stdin.read())


def ask_user(question, *options):
    """Ask the user a question.
	Parameters:
	- question: the string to ask the user
	- options: arbitrary list of arguments (at least 1)
	Returns the chosen option by the user or None if nothing was chosen (e.g. hit Escape).
	"""

    if len(options) == 0:
        value = "User needs to be able to select at least 1 answer"
        raise _IPyException(value)
    global _ui_factory
    return _AskUser(_ui_factory.mainroot, question, options).answer


class _Factory():
    def __init__(self):
        self.mainroot = _tk.Tk()
        self.mainroot.withdraw()
        self.mainroot.update()


class _AskInput(object):
    def __init__(self, mainroot):
        root = _tk.Toplevel(mainroot)
        root.withdraw()
        self.f = _tkFileDialog.askopenfilename(parent=root)
        if self.f != '':
            _sys.stdin = open(self.f)
        root.destroy()


class _AskUser(object):
    def __init__(self, mainroot, question, options):
        root = _tk.Toplevel(mainroot)
        root.withdraw()
        dg = _Dialog.Dialog(None,
                            title="",
                            text=question,
                            default=0,
                            bitmap=_tkMessageBox.QUESTION,
                            strings=options)
        self.answer = options[dg.num]
        root.destroy()


_ui_factory = _Factory()


class LifeUserInterface(object):
    def __init__(self, width, height, scale=1.0):
        """This class starts the LifeUserInterface.
		Constants:
		- DEAD
		- ALIVE

		Parameters for the class:
		- width: at least 1
		- height: at least 1

		Optional parameters:
		- scale: 0.25 to 1.0
		"""

        _verify_int(width, "Width", 1)
        _verify_int(height, "Height", 1)
        _verify_float(scale, 'Scale', 0.25, 1.0)
        global _ui_factory
        self.life_interface = _Life(width, height, _ui_factory.mainroot, scale)
        self.DEAD = _Life.DEAD
        self.ALIVE = _Life.ALIVE

    def place(self, x, y, color):
        """Place a Life piece (defined by 'color') on the given X and Y coordinates.
		"""

        _verify_int(x, 'X', 0, self.life_interface.width - 1)
        _verify_int(y, 'Y', 0, self.life_interface.height - 1)
        # 0 = empty, 1 = dead, 2 = alive
        _verify_int(color, 'Color', 0, 2)
        self.life_interface.place(x, y, color)

    def clear(self):
        """Clears the display.
		Note: this does not clear the text area!
		"""

        self.life_interface.clear()

    def show(self):
        """Show the changes made to the display (i.e. after calling place or clear)
		"""

        self.life_interface.show()

    def get_event(self):
        """Returns an event generated from the display.
		The returned object has 2 properties:
		- name: holds the group which the event belongs to.
		- data: holds useful information for the user.
		"""

        return self.life_interface.get_event()

    def set_animation_speed(self, fps):
        """Set an event to repeat 'fps' times per second.
		If the value is set to 0 or less, the repeating will halt.
		In theory the maximum value is 1000, but this depends on activity of the system.

		The generated events (available by using get_event) have these properties:
		- name: 'alarm'.
		- data: 'refresh'.
		"""

        _verify_float(fps, "Animation speed")
        self.life_interface.set_animation_speed(fps)

    def print_(self, text):
        """Print text to the text area on the display.
		This function does not add a trailing newline by itself.
		"""

        _verify_str(text, "Text")
        self.life_interface.print_(text)

    def clear_text(self):
        """Clears the text area on the display.
		"""

        self.life_interface.clear_text()

    def wait(self, ms):
        """Let your program wait for an amount of milliseconds.

		This function only guarantees that it will wait at least this amount of time.
		If the system, i.e., is too busy, then this time might increase.
		- Python time module.
		"""

        _verify_int(ms, "Waiting time", 0)
        self.life_interface.wait(ms)

    def random(self, maximum):
        """Picks a random integer ranging from 0 <= x < maximum
		Minimum for maximum is 1
		"""

        _verify_int(maximum, 'Random', 1)
        return self.life_interface.random(maximum)

    def close(self):
        """Closes the display and stops your program.
		"""

        self.life_interface.close()

    def stay_open(self):
        """Force the window to remain open.
		Only has effect on Mac OS to prevent the window from closing after the execution finishes.

		Make sure that this is the last statement you call when including it because the code does NOT continue after this.
		"""

        global _ui_factory
        _ui_factory.mainroot.mainloop()


class _Life(object):
    # one cannot prevent users from editing 'constants', as constants simply do not exist in Python
    DEAD = 0
    ALIVE = 1

    BACKGROUND = "#000000"

    def __init__(self, width, height, mainroot, scale=1.0):
        # create queue to store changes to placings
        self.to_show_queue = _Queue.Queue(maxsize=0)
        self.event_queue = _Queue.Queue(maxsize=0)

        # copy params
        self.width = width
        self.height = height
        self.scale = scale

        # start the main window
        self.root = _tk.Toplevel(mainroot)
        self.root.title("LifeUserInterface")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.bind("<Escape>", self.callback)
        self.root.resizable(False, False)

        # calculate sizes
        self.size_per_coord = int(25 * scale)
        self.text_height = int(100 * scale)

        # create main frame
        self.frame = _tk.Frame(self.root, width=self.size_per_coord * self.width,
                               height=self.size_per_coord * self.height + self.text_height)
        self.frame.pack_propagate(0)
        self.frame.pack()

        # create board to hold references to snake-pieces
        self.dead_board = []  # for storing references to create_image
        self.alive_board = []
        self.img_refs = []  # for storing references to images - order: dead, alive

        # create and fill the canvas --> paintable area
        self.c = _tk.Canvas(self.frame, width=self.size_per_coord * self.width,
                            height=self.size_per_coord * self.height, bg=self.BACKGROUND, bd=0, highlightthickness=0)
        self.c.pack()
        self.last_x = -1  # used to generate mouseOver/Exit events
        self.last_y = -1  # used to generate mouseOver/Exit events
        self.fill_canvas()

        # create the textholder
        self.scrollbar = _tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
        self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
        self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
        self.scrollbar.config(command=self.textarea.yview)
        self.textarea.config(state=_tk.DISABLED)

        self.interval = 0
        self.alarm_speed = 0
        self.timer = self.milliseconds()
        global _ui_factory
        _ui_factory.mainroot.update()

    def callback(self, event=None):
        self.root.destroy()
        _os._exit(0)

    def milliseconds(self):
        return _time.time() * 1000

    def place(self, x, y, color):
        element = _LifeHolder(x, y, color)
        self.to_show_queue.put(element)

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.place(x, y, self.DEAD)

    def show(self):
        try:
            while True:
                element = self.to_show_queue.get_nowait()
                position = []
                position.append(self.dead_board[element.x][element.y])
                position.append(self.alive_board[element.x][element.y])
                for i in range(len(position)):
                    if element.color == i:
                        for e in position[i]:
                            self.c.itemconfig(e, state=_tk.NORMAL)
                    else:
                        for e in position[i]:
                            self.c.itemconfig(e, state=_tk.HIDDEN)
        except _Queue.Empty:
            pass
        global _ui_factory
        _ui_factory.mainroot.update()

    def get_event(self):
        global _ui_factory
        _ui_factory.mainroot.update()
        while True:
            try:
                self.refresh_event()
                event = self.event_queue.get_nowait()
                return event
            except _Queue.Empty:
                wait_time = min(self.interval, 10)
                self.wait(wait_time)
                _ui_factory.mainroot.update()

    def set_animation_speed(self, fps):
        current_time = self.milliseconds()
        if fps <= 0:
            self.interval = 0
            self.timer = current_time
            return
        if fps > 1000:
            fps = 1000
        self.interval = int(1000.0 / fps)
        self.refresh_event()

    def print_(self, text):
        self.textarea.config(state=_tk.NORMAL)
        self.textarea.insert(_tk.END, text)
        self.textarea.see(_tk.END)
        self.textarea.config(state=_tk.DISABLED)
        global _ui_factory
        _ui_factory.mainroot.update()

    def clear_text(self):
        self.textarea.config(state=_tk.NORMAL)
        self.textarea.delete(1.0, _tk.END)
        self.textarea.see(_tk.END)
        self.textarea.config(state=_tk.DISABLED)
        global _ui_factory
        _ui_factory.mainroot.update()

    def wait(self, ms):
        try:
            _time.sleep(ms * 0.001)
        except:
            self.close()

    def close(self):
        self.root.destroy()


    def random(self, maximum=1):
        return int(_random.random() * maximum)

    def create_piece(self, x0, y0, img, state_):
        result = []
        if img == self.DEAD:
            r = 255
            g = 255
            b = 255
            x1 = x0
            y1 = y0
            # -1 from the second coordinate because the bottom and right borders are 1 pixel outside the boundary
            x2 = x0 + self.size_per_coord - 1
            y2 = y0 + self.size_per_coord - 1
            result.append(
                self.c.create_rectangle(x1, y1, x2, y2, state=state_, fill="#%02X%02X%02X" % (r, g, b), width=1))
        if img == self.ALIVE:
            r = 0
            g = 0
            b = 255
            x1 = x0
            y1 = y0
            # -1 from the second coordinate because the bottom and right borders are 1 pixel outside the boundary
            x2 = x0 + self.size_per_coord - 1
            y2 = y0 + self.size_per_coord - 1
            result.append(
                self.c.create_rectangle(x1, y1, x2, y2, state=state_, fill="#%02X%02X%02X" % (r, g, b), width=1))

        return result

    def create_life_pieces(self):
        imgtype = self.DEAD, self.ALIVE
        boards = self.dead_board, self.alive_board
        for n in range(len(boards)):
            for i in range(self.width):
                boards[n].append([])
                for j in range(self.height):
                    x0 = self.size_per_coord * i
                    y0 = self.size_per_coord * j
                    state_ = _tk.HIDDEN
                    if n == 0:
                        state_ = _tk.NORMAL
                    img = self.create_piece(x0, y0, imgtype[n], state_)
                    boards[n][i].append(img)

    def fill_canvas(self):
        self.bind_events()
        self.create_life_pieces()

    def motion_event(self, event):
        if not self.mouse_on_screen:
            return
        x_old = self.last_x
        y_old = self.last_y
        x_new = event.x / self.size_per_coord
        y_new = event.y / self.size_per_coord
        x_change = int(x_old) != int(x_new)
        y_change = int(y_old) != int(y_new)
        if x_change or y_change:
            self.generate_event("mouseexit", "%d %d" % (x_old, y_old))
            self.generate_event("mouseover", "%d %d" % (x_new, y_new))
            self.last_x = x_new
            self.last_y = y_new

    def enter_window_event(self, event):
        x_new = event.x / self.size_per_coord
        y_new = event.y / self.size_per_coord
        self.generate_event("mouseover", "%d %d" % (x_new, y_new))
        self.last_x = x_new
        self.last_y = y_new
        self.mouse_on_screen = True

    def leave_window_event(self, event):
        self.generate_event("mouseexit", "%d %d" % (self.last_x, self.last_y))
        self.mouse_on_screen = False

    def alt_number_event(self, event):
        if event.char == event.keysym:
            if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                self.generate_event("alt_number", event.char)

    def key_event(self, event):
        if event.char == event.keysym:
            if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                self.generate_event("number", event.char)
            elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
                self.generate_event("letter", event.char)
            elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
                self.generate_event("letter", event.char)
            else:
                self.generate_event("other", event.char)
        elif event.keysym == 'Up':
            self.generate_event("arrow", "u")
        elif event.keysym == 'Down':
            self.generate_event("arrow", "d")
        elif event.keysym == 'Left':
            self.generate_event("arrow", "l")
        elif event.keysym == 'Right':
            self.generate_event("arrow", "r")
        elif event.keysym == 'Multi_Key':
            return
        elif event.keysym == 'Caps_Lock':
            self.generate_event("other", "caps lock")
        elif event.keysym == 'Num_Lock':
            self.generate_event("other", "num lock")
        elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
            self.generate_event("other", "shift")
        elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
            self.generate_event("other", "control")
        elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
            self.generate_event("other", "alt")
        else:
            self.generate_event("other", event.keysym)

    def click_event(self, event):
        x = event.x / self.size_per_coord
        y = event.y / self.size_per_coord
        self.generate_event("click", "%d %d" % (x, y))

    def refresh_event(self):
        current_time = self.milliseconds()
        threshold = current_time - self.timer - self.interval
        if threshold >= 0 and self.interval > 0:
            self.generate_event("alarm", "refresh")
            self.timer = current_time

    def generate_event(self, name, data):
        event = Event(name, data)
        self.event_queue.put(event)

    def bind_events(self):
        self.c.focus_set()  # to redirect keyboard input to this widget
        self.c.bind("<Motion>", self.motion_event)
        self.c.bind("<Enter>", self.enter_window_event)
        self.c.bind("<Leave>", self.leave_window_event)
        self.c.bind("<Alt-Key>", self.alt_number_event)
        self.c.bind("<Key>", self.key_event)
        self.c.bind("<Button-1>", self.click_event)


class Event(object):
    def __init__(self, name, data):
        """This class holds the name and data for each event in their respective variables.
		Variables:
		- name
		- data

		Example to access with SnakeUserInterface:

		ui = SnakeUserInterface(5,5) # 5 by 5 grid for testing purposes
		your_variable = ui.get_event() # code will block untill an event comes
		# your_variable now points to an event
		print your_variable.name, your_variable.data

		List of events:
		- name: mouseover
		  data: x and y coordinates (as integers), separated by a space
			  generated when mouse goes over a coordinate on the window
		- name: mouseexit
		  data: x and y coordinates (as integers), separated by a space
			  generated when mouse exits a coordinate on the window
		- name: click
		  data: x and y coordinates (as integers), separated by a space
			  generated when the user clicks on a coordinate on the window
		- name: alarm
		  data: refresh
			  generated as often per second as the user set the animation speed to; note that the data is exactly as it says: "refresh"
		- name: letter
		  data: the letter that got pressed
			  generated when the user presses on a letter (A to Z; can be lowercase or uppercase depending on shift/caps lock)
		- name: number
		  data: the number (as a string) that got pressed
			  generated when the user presses on a number (0 to 9)
		- name: alt_number
		  data: the number (as a string) that got pressed
			  generated when the user presses on a number (0 to 9) while at the same time pressing the Alt key
		- name: arrow
		  data: the arrow key that got pressed, given by a single letter
			  generated when the user presses on an arrow key, data is then one of: l, r, u, d
		- name: other
		  data: data depends on key pressed
			  generated when the user pressed a different key than those described above
			  possible data:
			  - caps_lock
			  - num_lock
			  - alt
			  - control
			  - shift
			  more data can exist and are recorded (read: they generate events), but not documented
		"""
        self.name = name
        self.data = data
