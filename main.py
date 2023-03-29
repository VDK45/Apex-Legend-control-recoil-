# -*- coding: utf-8 -*-

import os
import json
import sys
import threading
import time
import win32api  #  pip install pywin32
import win32con
import winsound
import ctypes
from image_search import get_screen_area_as_image, load_image_from_file, search_image_in_image
from overlay_label import OverlayLabel
from keyboard_input import keyb_down, keyb_up
import pathlib
from pathlib import Path
import gui
from pynput.mouse import Button, Controller
import pyautogui



LMB = win32con.VK_LBUTTON
F4 = win32con.VK_F4
F10 = win32con.VK_F10
NUM_4 = win32con.VK_NUMPAD4
NUM_6 = win32con.VK_NUMPAD6
F1 = 0x70
L_MOUSE = 0x01
R_MOUSE = 0x02
TAB = 0x09
SPACE = 0x20
ESC = 0x1B
MINUS = 0xBD
L_CTRL = 0xA2
BUTTON_1 = 0x31
BUTTON_2 = 0x32
BUTTON_3 = 0x33
BUTTON_A = 0x41
BUTTON_D = 0x44
BUTTON_E = 0x45
BUTTON_G = 0x47
BUTTON_J = 0x4A
BUTTON_L = 0x4C
BUTTON_R = 0x52
enemy = True


EMPTY_WEAPONS_LIST = [
    {
        "name": "None",
        "rpm": 6000,
        "check_image": None,
        "check_area": [1352, 701, 1382, 731],
        "pattern": [
            [0,0],
        ]
    },
]

# for cursor detector
class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int),
                ('y', ctypes.c_int)]

class CURSORINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint),
                ('flags', ctypes.c_uint),
                ('hCursor', ctypes.c_void_p),
                ('ptScreenPos', POINT)]
               


def beep_on():
    winsound.Beep(2000, 100)


def beep_off():
    winsound.Beep(1000, 100)


def beep_exit():
    winsound.Beep(500, 500)


def mouse_move_relative(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)


def lmb_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def lmb_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def rmb_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)


def rmb_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def is_lmb_pressed():
    return win32api.GetKeyState(LMB) < 0
    
def is_lmb_release():
    return win32api.GetKeyState(LMB) > 0

def cursor_detector():
    # Load and set argument types
    GetCursorInfo = ctypes.windll.user32.GetCursorInfo
    GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
    # Initialize the output structure
    info = CURSORINFO()
    info.cbSize = ctypes.sizeof(info)
    # Do it!
    if GetCursorInfo(ctypes.byref(info)):
        if info.flags & 0x00000001:
            return True
        else:
            return False
    else:
        print("WARNING: Cursor detector is not running!")


def load_weapons():
    weapons_list = EMPTY_WEAPONS_LIST
    current_weapon_index = 0
    weapon_filepath = "./weapon_data/apex.json"
    #print("DEBUG: Opening and load data from {}".format(weapon_filepath))
    try:
        with open(weapon_filepath) as f:
            data = json.load(f)
            weapons_data = data["weapons"]
    except:
        print("ERROR: Can not open/read file with weapon data!")
        print("INFO: ERROR! Use default EMPTY_WEAPONS_LIST. Check data files!")
        return weapons_list, current_weapon_index

    weapons_list = weapons_data

    for i, weapon in enumerate(weapons_list):
        if weapon["check_image"]:
            image = load_image_from_file("./weapon_data/apex_img\{}".format(weapon["check_image"]))
            weapons_list[i]["image"] = image
        else:
            weapons_list[i]["image"] = None

    return weapons_list, current_weapon_index


def toggle_recoil(no_recoil):
    if no_recoil == True:
        beep_off()
    else:
        beep_on()
    return not no_recoil


def prev_weapon(weapons_list, current_weapon_index):
    if current_weapon_index < 1:
        current_weapon_index = len(weapons_list) - 1
    else:
        current_weapon_index -= 1
    return current_weapon_index


def next_weapon(weapons_list, current_weapon_index):
    if current_weapon_index > len(weapons_list) - 2:
        current_weapon_index = 0
    else:
        current_weapon_index += 1
    return current_weapon_index


def get_tick(rpm):
    rps = rpm/60
    mstick = 1000.0/rps
    stick = round(mstick/1000, 3)
    return stick


def construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil):
    recoil_data = "ON" if no_recoil else "OFF/GRENADE"
    bg_data = "#acffac" if no_recoil else "#ffacac"
    recoil_string = "No recoil+: {}".format(recoil_data)
    weapon_string = "Weapon: {}".format(weapons_list[current_weapon_index]["name"])
    length = max(len(recoil_string), len(weapon_string))
    overlay_string = "{}\n{}".format(recoil_string.ljust(length), weapon_string.ljust(length))
    overlay.set_bg(bg_data)
    overlay.set_text(overlay_string)


def process_no_recoil(overlay, weapons_list, current_weapon_index, no_recoil):
    global M_SENS
    shot_index = 0
    shot_tick = get_tick(weapons_list[current_weapon_index]["rpm"])
    while is_lmb_pressed():
        current_pattern = weapons_list[current_weapon_index]["pattern"]
        

        if shot_index < len(current_pattern) - 1:
            dx = -(current_pattern[shot_index][0] + gui.M_SENS)
            dy = -(current_pattern[shot_index][1] + gui.M_SENS)
            mouse_move_relative(dx, dy)
            time.sleep(shot_tick)
            shot_index += 1
            construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil)
            

def detect_current_weapon(weapons_list):
    for index, weapon in enumerate(weapons_list):
        if weapon["image"] is not None:
            found_xy = None
            try:
                image_to_check = get_screen_area_as_image(weapon["check_area"])
                found_xy = search_image_in_image(weapon["image"], image_to_check)
            except:
                print("Can not read images. Check folder weapon_data!")
            if found_xy:
                return index
    return None


class WeaponDetectorThread(threading.Thread):
    def __init__(self, weapon_list):
        threading.Thread.__init__(self)
        self.weapon_list = weapon_list
        self.out = None
        self.no_recoil = False
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            if self.no_recoil:
                weapon_autodetect = detect_current_weapon(self.weapon_list)
                self.out = weapon_autodetect
            time.sleep(0.01)

    def terminate(self):
        self.shutdown = True


run = True
lmb_pressing = False
mouse = Controller()
#locker = threading.Lock()
lmb_infinity = False


def listen_lmb():
    global lmb_pressing
    global enemy
    enemy = False
    while True:
        time.sleep(0.001)
        if win32api.GetAsyncKeyState(BUTTON_E):
            enemy = False
        if (win32api.GetAsyncKeyState(0x01)&0x8000 > 0):
            lmb_pressing = True
            if enemy and gui.ENEMY:
                # press J ping ENEMY HERE
                keyb_down(BUTTON_J)
                time.sleep(0.01)
                keyb_up(BUTTON_J)
                enemy = False
        else:
            lmb_pressing = False
            enemy = True
            

def click_lmb():
    global lmb_pressing
    while True:
        time.sleep(0.01)
        if lmb_pressing and lmb_infinity:
            keyb_down(MINUS)
            time.sleep(0.01)
            keyb_up(MINUS)
            time.sleep(0.01)
            mouse_move_relative(0, 38)
        elif lmb_pressing and not lmb_infinity:
            keyb_down(MINUS)
        else:
            keyb_up(MINUS)

            

def main():
    global lmb_pressing
    global lmb_infinity
    global enemy
    couldown = 0
    f1_timer = True
    CYCLE_WEAPON = True
    SHOP = True
    running = True
    no_recoil = False
    weapons_list, current_weapon_index = load_weapons()
    overlay = OverlayLabel()
    overlay.set_size(22, 2)  # size in symbols
    print("INFO: Starting WeaponDetector daemon...")
    weapon_detector = WeaponDetectorThread(weapons_list)
    # weapon_detector.setDaemon(True)
    weapon_detector.start()
    print("INFO: Ready!")
    print("INFO: F10 - Exit program")
    print("INFO: FULL VERSION")
    no_recoil = toggle_recoil(no_recoil)
    weapon_detector.no_recoil = no_recoil
    state_left = win32api.GetKeyState(L_MOUSE)  # L mouse
    state_right = win32api.GetKeyState(R_MOUSE)  # R mouse
    listen_thread = threading.Thread(target=listen_lmb, daemon=True)
    listen_thread.start()
    click_thread = threading.Thread(target=click_lmb, daemon=True)
    click_thread.start()
    
    while running:
        time.sleep(0.001)
        # weapon = current_weapon_index
        
        # Press F10 EXIT / Press F10 toggle recoil
        if win32api.GetAsyncKeyState(F10):
            running = not running
            beep_exit()
            run = False
            weapon_detector.terminate()
            print("INFO: Exiting!")
            time.sleep(0.1)
        elif win32api.GetAsyncKeyState(F4):
            no_recoil = toggle_recoil(no_recoil)
            weapon_detector.no_recoil = no_recoil
            time.sleep(0.1)

        # NORECOIL process
        weapons_list, current_weapon_index = load_weapons()
        if weapon_detector.out is not None:
            current_weapon_index = weapon_detector.out
        construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil)
        if is_lmb_pressed() and no_recoil and not cursor_detector() and not lmb_infinity and gui.RECOIL:  
            process_no_recoil(overlay, weapons_list, current_weapon_index, no_recoil)
            
        # In menu turn off infinity M1 / Dead box moving Left and Right
        # Press TAB / ESC / CTRL Stop moving L and R
        if win32api.GetAsyncKeyState(TAB) \
                or win32api.GetAsyncKeyState(ESC) \
                or win32api.GetAsyncKeyState(L_CTRL):
            SHOP = False
        elif win32api.GetAsyncKeyState(BUTTON_E):
            SHOP = True
        elif current_weapon_index == 1 and gui.SHOP and SHOP :
            lmb_infinity = False
            keyb_down(BUTTON_A)
            time.sleep(0.1)
            keyb_up(BUTTON_A)
            time.sleep(0.01)
            keyb_down(BUTTON_D)
            time.sleep(0.1)
            keyb_up(BUTTON_D)
            
        # Auto press F1
        now = time.time()
        if now >= couldown:
            f1_timer = True
        if current_weapon_index == 2 and f1_timer and gui.F_ONE:  # F1
            f1_timer = False
            couldown = time.time() + 2
            keyb_down(F1)
            time.sleep(0.02)
            keyb_up(F1)
        # Auto press spaces in menu
        elif current_weapon_index == 3:  # Menu 
            lmb_infinity = False
            keyb_down(SPACE)
            time.sleep(0.2)
            keyb_up(SPACE)
        
        # # Auto RELOAD/CYCLE WEAPON
        if win32api.GetAsyncKeyState(BUTTON_1) < 0 \
                        or win32api.GetAsyncKeyState(BUTTON_2) < 0 \
                        or win32api.GetAsyncKeyState(BUTTON_G) \
                        or win32api.GetAsyncKeyState(BUTTON_R):
            CYCLE_WEAPON = False
        elif current_weapon_index == 5 and gui.RELOAD :  # Fast reload
            keyb_up(L_MOUSE)
            keyb_up(MINUS)
            keyb_down(BUTTON_R)
            time.sleep(0.01)
            keyb_up(BUTTON_R)
        elif current_weapon_index == 4 and CYCLE_WEAPON and gui.RELOAD :  # Cycle weapon
            keyb_up(L_MOUSE)
            keyb_up(MINUS)
            CYCLE_WEAPON = False
            keyb_down(BUTTON_L)
            time.sleep(0.01)
            keyb_up(BUTTON_L)
        elif current_weapon_index == 4 and not CYCLE_WEAPON and gui.RELOAD :   # Reload
            keyb_up(L_MOUSE)
            keyb_up(MINUS)
            keyb_down(BUTTON_R)
            time.sleep(0.01)
            keyb_up(BUTTON_R)
        
        # Press G no recoil OFF
        mouse_1 = win32api.GetKeyState(L_MOUSE)
        if win32api.GetKeyState(BUTTON_G) < 0:
            no_recoil = False
        # Press 1/2/R/E no recoil ON
        elif win32api.GetKeyState(BUTTON_1) < 0 or \
               win32api.GetKeyState(BUTTON_2) < 0 or \
               win32api.GetKeyState(BUTTON_R) < 0 or \
               win32api.GetKeyState(BUTTON_E) < 0:
            no_recoil = True
            is_lmb_release()
            keyb_up(L_MOUSE)
            keyb_up(MINUS)
            lmb_infinity = True
            current_weapon_index = 7  # One shot
        elif win32api.GetKeyState(TAB) < 0 or win32api.GetKeyState(ESC) < 0:
            current_weapon_index = 0
            
        # Press LMB no recoil ON
        if mouse_1 != state_left:  # mouse 1 release 
            state_left = mouse_1
            if mouse_1 >= 0:
                no_recoil = True
                CYCLE_WEAPON = True
                # current_weapon_index = 0 
            
        # P2020/G7 Scout/Hemlok/MASTIFF/Peacekeeper/
        # Prowler/P 30-30/Triple Take/ Infinity shots (auto single shot)
        if current_weapon_index == 0 and no_recoil:  # No weapon
            lmb_infinity = False
            enemy = False
        elif current_weapon_index == 6 and no_recoil:  # Bocec
            lmb_infinity = False
        elif current_weapon_index == 7 and no_recoil and gui.SINGLE \
        or current_weapon_index == 8 and no_recoil and gui.SINGLE \
        or current_weapon_index == 14 and no_recoil and gui.SINGLE \
        or current_weapon_index == 16 and no_recoil and gui.SINGLE \
        or current_weapon_index == 21 and no_recoil and gui.SINGLE \
        or current_weapon_index == 22 and no_recoil and gui.SINGLE \
        or current_weapon_index == 23 and no_recoil and gui.SINGLE \
        or current_weapon_index == 24 and no_recoil and gui.SINGLE \
        or current_weapon_index == 30 and no_recoil and gui.SINGLE \
        or current_weapon_index == 31 and no_recoil and gui.SINGLE \
        or current_weapon_index == 34 and no_recoil and gui.SINGLE :  
            lmb_infinity = True
        else:
            lmb_infinity = False
            


if __name__ == "__main__":
    print("                       ")
    print("                       ")
    print("***************** ВАЖНО  ********************")
    print("Внимание: Только для английской версии")
    print("Внимание: Разрешение экрана только: 1920 × 1080")
    print("Внимание: Стрелать только клавишей - (МИНУС)")
    print("Внимание: Клавиша J для пометки врагов")
    print("Внимание: Чтобы overlay отображался играть в окне или без рамки (Не в польноэкраном режиме)")
    print("Не закрывайте это окно!")
    print("                       ")
    print("                       ")
    
    print("***************** IMPORTANT  ********************")
    print("Attention: English version only")
    print("Attention: Resolution screen only: 1920×1080")
    print("Attention: Shoot only with the - (MINUS) button")
    print("Attention: J key to ping enemies")
    print("Attention: To have the overlay displayed play in a window or without a border (Not in full screen mode)")
    print("Don't close this window!")
    
    main()
    run = False
    
