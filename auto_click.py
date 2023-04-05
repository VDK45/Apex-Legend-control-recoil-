import win32api
import win32con
import time
from pynput.mouse import Button, Controller
import threading


def mouse_move_relative(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)


run = True
flag = False
mouse = Controller()
locker = threading.Lock()
LMB = win32con.VK_LBUTTON


def is_lmb_pressed():
    return win32api.GetKeyState(LMB) < 0


def is_lmb_release():
    return win32api.GetKeyState(LMB) > 0


def listen_lmb():
    global flag
    while run:
        time.sleep(0.01)
        if (win32api.GetAsyncKeyState(0x01) & 0x8000 > 0):
        # if is_lmb_pressed():
            locker.acquire()
            flag = True
            locker.release()
        else:
            locker.acquire()
            flag = False
            locker.release()


def click_lmb():
    global flag
    while run:
        if flag:
            mouse.press(Button.left)
            time.sleep(0.1)
            mouse.release(Button.left)
            mouse_move_relative(0, 38)


click_thread = threading.Thread(target=click_lmb)
click_thread.start()

listen_thread = threading.Thread(target=listen_lmb)
listen_thread.start()
