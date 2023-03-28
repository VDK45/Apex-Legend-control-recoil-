import tkinter as tk
from random import randint
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

photo = resource_path('weapon_data/apex_full.png')



window = tk.Tk()
bg_color = '#A0ACB0'
height = 500
weight = 750
photo = tk.PhotoImage(file=photo)
window.iconphoto(False, photo)
window.config(bg=bg_color)
window.title("Option:")
# Высота х ширина + (отступ по x+100) + (отступ по y+100)
window.geometry(f"{height}x{weight}+100+100")
window.minsize(250, 350)
window.maxsize(500, 600)
window.resizable(False, False)
sens_value = 7.0
RECOIL = True
SHOP = True
F_ONE = True
M_SENS = 0
SINGLE = True
RELOAD = True
ENEMY = True

def select_recoil_var():
    select = recoil_var.get()
    global RECOIL
    if select:
        print('Recoil ON')
        recoil_text.set(f'Control recoil ON')
        RECOIL = True
        recoil_show.config(bg = "#3f91e8")
    elif select == False:
        print('Recoil OFF')
        recoil_text.set(f'Control recoil OFF')
        RECOIL = False
        recoil_show.config(bg = "#d92121")

recoil_var = tk.BooleanVar()
recoil_text = tk.StringVar()
recoil_var.set(True)
recoil_text.set(f'Control recoil ON')
                    
recoil_button_off = tk.Radiobutton(window, text='OFF', variable=recoil_var, value=False, command=select_recoil_var, 
                    bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
recoil_button_on = tk.Radiobutton(window, text='ON', variable=recoil_var, value=True, command=select_recoil_var,
                    bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
recoil_show = tk.Label(window, textvariable=recoil_text,
                    bg="#3f91e8",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="center",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.CENTER)  # Выровнять текст по центру)
                    

recoil_show.place(x=25, y=20)
recoil_button_off.place(x=40, y=70)
recoil_button_on.place(x=130, y=70)


def mouse_sen_plus():
    global sens_value 
    global M_SENS
    if sens_value < 12:
        sens_value += 0.2
        M_SENS -= 0.5
        label_1.config(text = f"Recoil sensitivity: {round(sens_value, 1)}")
    else:
        sens_value = 12
    


button_1 = tk.Button(window, text="Recoil sensitivity +",
                     command=mouse_sen_plus,
                     bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=15,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT 
                     )



def mouse_sen_minus():
    global sens_value 
    global M_SENS
    if sens_value > 0.2:
        sens_value -= 0.2
        M_SENS += 0.5
        label_1.config(text = f"Recoil sensitivity: {round(sens_value, 1)}")
    else:
        sens_value = 0.2
    
label_1 = tk.Label(window, text=f"""Recoil sensitivity: {round(sens_value)}""",
                    bg="#2FB7B3",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="se",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.RIGHT  # Выровнять тексты по правой стороне
                    )
                    


button_2 = tk.Button(window, text="Recoil sensitivity -",
                     command=mouse_sen_minus,
                     bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=15,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT 
                     )

button_1.place(x=45, y=120)
label_1.place(x=25, y=170)  
button_2.place(x=45, y=220)




def select_shop_var():
    select = shop_var.get()
    global SHOP
    if select:
        print('Shop ON')
        shop_text.set(f'Dead box / Shop ON')
        SHOP = True
        shop_show.config(bg = "#3f91e8")
    elif select == False:
        print('Shop OFF')
        shop_text.set(f'Dead box / Shop OFF')
        SHOP = False
        shop_show.config(bg = "#d92121")
    

shop_var = tk.BooleanVar()
shop_text = tk.StringVar()
shop_var.set(True)
shop_text.set(f'Dead box / Shop ON')
                    
shop_button_off = tk.Radiobutton(window, text='OFF', variable=shop_var, value=False, command=select_shop_var, 
                    bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
shop_button_on = tk.Radiobutton(window, text='ON', variable=shop_var, value=True, command=select_shop_var,
                    bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
shop_show = tk.Label(window, textvariable=shop_text,
                    bg="#3f91e8",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="center",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.CENTER)  # Выровнять текст по центру)
                    

shop_show.place(x=25, y=310)
shop_button_off.place(x=40, y=360)
shop_button_on.place(x=130, y=360)



def select_f1_var():
    select = f1_var.get()
    global F_ONE
    if select:
        print('F1 ON')
        f1_text.set(f'Auto press F1 ON')
        F_ONE = True
        f1_show.config(bg = "#3f91e8")
    elif select == False:
        print('F1 OFF')
        f1_text.set(f'Auto press F1 OFF')
        F_ONE = False
        f1_show.config(bg = "#d92121")
    

f1_var = tk.BooleanVar()
f1_text = tk.StringVar()
f1_var.set(True)
f1_text.set(f'Auto press F1 ON')
                    
f1_button_off = tk.Radiobutton(window, text='OFF', variable=f1_var, value=False, command=select_f1_var, 
                    bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
f1_button_on = tk.Radiobutton(window, text='ON', variable=f1_var, value=True, command=select_f1_var,
                    bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
f1_show = tk.Label(window, textvariable=f1_text,
                    bg="#3f91e8",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="center",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.CENTER)  # Выровнять текст по центру)
                    

f1_show.place(x=25, y=460)
f1_button_off.place(x=40, y=510)
f1_button_on.place(x=130, y=510)


def select_single_var():
    select = single_var.get()
    global SINGLE
    if select:
        print('single ON')
        single_text.set(f'Auto single shots ON')
        SINGLE = True
        single_show.config(bg = "#3f91e8")
    elif select == False:
        print('single OFF')
        single_text.set(f'Auto single shots OFF')
        SINGLE = False
        single_show.config(bg = "#d92121")
    

single_var = tk.BooleanVar()
single_text = tk.StringVar()
single_var.set(True)
single_text.set(f'Auto single shots ON')
                    
single_button_off = tk.Radiobutton(window, text='OFF', variable=single_var, value=False, command=select_single_var, 
                    bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
single_button_on = tk.Radiobutton(window, text='ON', variable=single_var, value=True, command=select_single_var,
                    bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
single_show = tk.Label(window, textvariable=single_text,
                    bg="#3f91e8",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="center",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.CENTER)  # Выровнять текст по центру)
                    

single_show.place(x=270, y=460)
single_button_off.place(x=280, y=510)
single_button_on.place(x=380, y=510)


def select_reload_var():
    select = reload_var.get()
    global RELOAD
    if select:
        print('reload ON')
        reload_text.set(f'Auto reload/cycle ON')
        RELOAD = True
        reload_show.config(bg = "#3f91e8")
    elif select == False:
        print('reload OFF')
        reload_text.set(f'Auto reload/cycle OFF')
        RELOAD = False
        reload_show.config(bg = "#d92121")
    

reload_var = tk.BooleanVar()
reload_text = tk.StringVar()
reload_var.set(True)
reload_text.set(f'Auto reload/cycle ON')
                    
reload_button_off = tk.Radiobutton(window, text='OFF', variable=reload_var, value=False, command=select_reload_var, 
                    bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
reload_button_on = tk.Radiobutton(window, text='ON', variable=reload_var, value=True, command=select_reload_var,
                    bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
reload_show = tk.Label(window, textvariable=reload_text,
                    bg="#3f91e8",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="center",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.CENTER)  # Выровнять текст по центру)
                    

reload_show.place(x=270, y=310)
reload_button_off.place(x=280, y=360)
reload_button_on.place(x=380, y=360)

def select_enemy_var():
    select = enemy_var.get()
    global ENEMY
    if select:
        print('enemy ON')
        enemy_text.set(f'Auto ping enemy  ON')
        ENEMY = True
        enemy_show.config(bg = "#3f91e8")
    elif select == False:
        print('enemy OFF')
        enemy_text.set(f'Auto ping enemy OFF')
        ENEMY = False
        enemy_show.config(bg = "#d92121")
    

enemy_var = tk.BooleanVar()
enemy_text = tk.StringVar()
enemy_var.set(True)
enemy_text.set(f'Auto ping enemy ON')
                    
enemy_button_off = tk.Radiobutton(window, text='OFF', variable=enemy_var, value=False, command=select_enemy_var, 
                    bg="#EFCFCF",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
enemy_button_on = tk.Radiobutton(window, text='ON', variable=enemy_var, value=True, command=select_enemy_var,
                    bg="#2FB773",
                    fg="black",
                    font=("Arial", 8, "bold"),
                    padx=15,  
                    pady=5,  
                    width=1,  
                    height=1,  
                    anchor="n",  
                    relief=tk.RAISED,  
                    bd=10,  
                    justify=tk.RIGHT )
enemy_show = tk.Label(window, textvariable=enemy_text,
                    bg="#3f91e8",
                    fg="black",
                    font=("Arial", 12, "bold"),
                    padx=15,  # Отступ текста от крайя по х
                    pady=5,  # Отступ текста от крайя по y
                    width=15,  # Ширина блока в символах
                    height=1,  # Высота блока в символах
                    anchor="center",  # n, ne, e, se, s, sw, w, nw, or center,
                    relief=tk.RAISED,  # Рамка вокруг блока
                    bd=10,  # Ширина рамки
                    justify=tk.CENTER)  # Выровнять текст по центру)
                    

enemy_show.place(x=270, y=20)
enemy_button_off.place(x=280, y=70)
enemy_button_on.place(x=380, y=70)


if __name__ == "__main__":
    window.mainloop()















