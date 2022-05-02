from math import e
from math import pi
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.widgets import TextBox, CheckButtons

start_func = 'e**(2*x)'

dots_num = 10

start_x = 0
end_x = 1


def f(x): return eval(start_func)


fig, ax = plt.subplots()

added_patches = [[], [], []]


def clear_patches():
    [[patch.remove() for patch in patches_types]
     for patches_types in added_patches]
    [patches_types.clear() for patches_types in added_patches]


def draw_func(text):
    global f
    global start_func
    start_func = text
    clear_patches()
    def f(x): return eval(start_func)
    x = np.arange(start_x, end_x, (end_x - start_x) / 100)
    y = [f(xi) for xi in x]
    ax.clear()
    ax.plot(x, y)
    ax.relim()
    ax.autoscale_view()


def apply_squares(text):
    global dots_num
    dots_num = int(text)
    areas = [0, 0, 0]
    dx = (end_x - start_x)/dots_num
    check_statuses = check.get_status()
    clear_patches()
    for check_num in range(len(check_statuses)):
        if check_statuses[check_num]:
            for i in range(dots_num):
                x = start_x + (i/dots_num) * (end_x - start_x)
                dy = f(x + (check_num / 2) * dx)
                areas[check_num] += dx*dy
                added_patches[check_num].append(patches.Rectangle(
                    (x, 0), dx, dy, edgecolor='blue', fill=False))
                ax.add_patch(added_patches[check_num][i])
    fig.suptitle(
        f'Sн = {areas[0]}; Sс = {areas[1]}; Sк = {areas[2]}', fontsize=10)
    plt.pause(0)


def squares_switch(label):
    apply_squares(dots_num)


def set_start_x(text):
    global start_x
    start_x = float(text)
    draw_func(start_func)


def set_end_x(text):
    global end_x
    end_x = float(text)
    draw_func(start_func)


plt.subplots_adjust(left=0.3, bottom=0.3)

func_text = TextBox(plt.axes([0.6, 0.15, 0.2, 0.075]),
                    'Функция ', start_func, textalignment='center')
func_text.on_submit(draw_func)

dots_num_text = TextBox(plt.axes([0.3, 0.15, 0.1, 0.075]),
                        'Число точек разбиения ', initial=str(dots_num), textalignment='center')
dots_num_text.on_submit(apply_squares)

start_x_text = TextBox(plt.axes([0.39, 0.05, 0.1, 0.075]),
                       'X in ', initial=str(start_x), textalignment='center')
start_x_text.on_submit(set_start_x)

end_x_text = TextBox(plt.axes([0.5, 0.05, 0.1, 0.075]),
                     ';', initial=str(end_x), textalignment='center')
end_x_text.on_submit(set_end_x)

rax = plt.axes([0.05, 0.4, 0.2, 0.15])
labels = ['Начало', 'Середина', 'Конец']
check = CheckButtons(rax, labels)
check.on_clicked(squares_switch)

draw_func(start_func)

plt.show(block=True)
