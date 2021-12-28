import tests_life
from lifeui import *

pause = False
show_ui = True
frame_nr = 0
period = None # set below


def draw(ui, gen):
    ui.clear()
    for x in range(gen.width()):
        for y in range(gen.height()):
            if gen.is_alive(x, y):
                ui.place(x, y, ui.ALIVE)


def print_period(ui, life_history):
    if life_history.dies_out():
        ui.print_("Dies out after %d steps \n" % life_history.nr_generations())
    period = life_history.period()
    if period == 1:
        ui.print_("Becomes stable after %d steps " % life_history.nr_generations())
    elif not (period is None):
        ui.print_("Period %d after %d steps" % (period, life_history.nr_generations() - period))


def handle_events(event):
    global pause, frame_nr, period, show_ui
    if not pause and event.name == "alarm" and event.data == "refresh":
        frame_nr += 1
    elif event.name == "other" and event.data == "space":
        pause = not pause
    elif event.name == "arrow" and event.data == "r":
        frame_nr += 1
    elif event.name == "arrow" and event.data == "l":
        frame_nr -= 1
    elif event.name == "letter" and event.data == "q":
        show_ui = False


def handle_frame_nr(life_history):
    global frame_nr, pause
    if frame_nr == life_history.nr_generations():
        if not (period is None) and period != 1:
            frame_nr = frame_nr - period
        else:
            frame_nr = frame_nr - 1
            pause = True
    if frame_nr < 0:
        frame_nr = 0


def visualize(ui, life_history):
    global pause, show_ui, period, frame_nr
    pause = True
    show_ui = True
    period = life_history.period()
    print_period(ui, life_history)
    frame_nr = 0
    while show_ui:
        draw(ui, life_history.get_generation(frame_nr))
        ui.show()
        handle_events(ui.get_event())
        handle_frame_nr(life_history)
    ui.close()


WIDTH, HEIGHT = 9, 9
SCALE = 1
FPS = 5
MAX_STEPS = 100


def beautify(board):
    str = ""
    for row in board:
        for v in row:
            str += "x" if v else " "
        str += "\n"
    return str


def visualize_test(test):
    history = LifeHistory(LifeGeneration(test))
    history.play_out(MAX_STEPS)
    ui = LifeUserInterface(WIDTH, HEIGHT, SCALE)
    ui.set_animation_speed(FPS)
    visualize(ui, history)


from tests_life import *
from life import *

# these examples are run in order. Press q to go to the next one.
#visualize_test(tests_life.input1[0])
visualize_test(tests_life.input2[0])
visualize_test(tests_life.input3[0])
visualize_test(tests_life.stable[0])
visualize_test(tests_life.dies[0])
visualize_test(tests_life.period2[0])
visualize_test(tests_life.period14[0])
