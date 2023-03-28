# -*- coding: utf-8 -*-

import pywintypes
import tkinter
import win32api
import win32con


class OverlayLabel:
    def __init__(self, text="IPSUM DOLOREM", pos="BR"):
        self.text = text
        self.pos = pos
        self.fg = "black"
        self.bg = "#f1f2f2"  # default transparent color
        self.width = 20
        self.height = 20

        tk = tkinter.Tk()
        self.label = tkinter.Label(tk, anchor="w")
        self.label.config(font=("Consolas", 8))
        self.label.master.overrideredirect(True)
        self.label.master.lift()
        self.label.master.wm_attributes("-topmost", True)
        self.label.master.wm_attributes("-disabled", True)
        self.label.master.wm_attributes("-transparentcolor", "#f1f2f3")

        hWindow = pywintypes.HANDLE(int(self.label.master.frame(), 16))
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | \
                  win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

        self.label.pack()
        self.update()

    def update(self):
        self.label.config(text=self.text)
        self.label.config(fg=self.fg)
        if self.bg == "none":
            self.label.config(bg="#f1f2f2")
        else:
            self.label.config(bg=self.bg)

        self.label.update()
        self.width = self.label.winfo_width()
        self.height = self.label.winfo_height()

        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(30)

        if self.pos[0] == "T":
            y = 0
        elif self.pos[0] == "M":
            y = screen_height / 2 - self.height / 2
        else:
            y = screen_height - self.height

        if self.pos[1] == "L":
            x = 0
        elif self.pos[1] == "C":
            x = screen_width / 2 - self.width / 2
        else:
            x = screen_width - self.width

        self.label.master.geometry("+{}+{}".format(int(x), int(y)))
        self.label.update()

    def set_text(self, text):
        self.text = text
        self.update()

    def set_bg(self, bg):
        self.bg = bg
        self.update()

    def set_fg(self, fg):
        self.fg = fg
        self.update()

    def set_pos(self, pos):
        self.pos = pos
        self.update()

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.label.config(width=self.width, height=self.height)
        self.update()
