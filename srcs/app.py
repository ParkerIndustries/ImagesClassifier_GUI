# -*- coding: utf-8 -*-

import sys
import os
import configparser
from time import time, localtime, strftime, sleep

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
import _tkinter
from PIL import Image, ImageTk

from srcs.const import *



class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.layers_list = {}

        self.bind("<KeyPress>", self.onKeyPress)
        self.bind("<KeyRelease>", self.onKeyRelease)

        self.devMode = False
        self.l_ctrl_pressed = False;

        self.title("Images Classifier GUI")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1000)

        style = ttk.Style()
        current_theme = style.theme_use()

        self.dir_open_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))
        self.dir_photos_pic = ImageTk.PhotoImage(Image.open('assets/dir_photos.png'))
        self.save_pic = ImageTk.PhotoImage(Image.open('assets/save.png'))

        self.cfg = configparser.ConfigParser()
        self.cfg.read(FILE_CONFIG)
        self.snap_path = StringVar()
        self.snap_path.set(self.cfg.get('paths', 'snap_path'))
        self.out_path = StringVar()
        self.out_path.set(self.cfg.get('paths', 'out_path'))

        self.options_but = Button(self, text="Options", font=("Helvetica", 16), command=self.open_options)
        self.options_but.grid(row=0, column=0, sticky="nw")

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=1, column=0, sticky='nsew')
        self.tabs.grid_columnconfigure(0, weight=1)
        self.tabs.grid_rowconfigure(0, weight=1)
        style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"padding": [20, 5]}}})

        self.first_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.first_tab, text=SNAP_NAME, compound=LEFT)
        self.first_tab.grid_columnconfigure(0, weight=1)
        self.first_tab.grid_rowconfigure(0, weight=1)
        self.second_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.second_tab, text=LABEL_NAME, compound=LEFT)
        self.second_tab.grid_columnconfigure(0, weight=1)
        self.second_tab.grid_rowconfigure(0, weight=1)
        self.third_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.third_tab, text=MODEL_NAME, compound=LEFT)
        self.third_tab.grid_columnconfigure(0, weight=1)
        self.third_tab.grid_rowconfigure(0, weight=1)
        self.fourth_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.fourth_tab, text=TRAIN_NAME, compound=LEFT)
        self.fourth_tab.grid_columnconfigure(0, weight=1)
        self.fourth_tab.grid_rowconfigure(0, weight=1)
        self.fifth_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.fifth_tab, text=TEST_NAME, compound=LEFT)
        self.fifth_tab.grid_columnconfigure(0, weight=1)
        self.fifth_tab.grid_rowconfigure(0, weight=1)

    def setDevMode(self, devMode):
        self.devMode = devMode

    def onKeyPress(self, event):
        """
        define action with keyboard shortcut
        """
        if self.devMode:
            print(YELLOW + 'key press: ' + EOC + event.keysym)
        if event.keysym == KEY_OPTION:
            self.open_options()
        elif event.keysym == KEY_QUIT:
            self.on_Quit()
        elif event.keysym == KEY_CTRL_L:
            self.l_ctrl_pressed = True;

        if self.l_ctrl_pressed == True:
            if event.keysym == KEY_NEXT_TAB:
                try:
                    self.tabs.select(self.tabs.index(self.tabs.select()) + 1)
                except _tkinter.TclError:
                    pass
            elif event.keysym == KEY_PREV_TAB:
                try:
                    self.tabs.select(self.tabs.index(self.tabs.select()) - 1)
                except _tkinter.TclError:
                    pass

        # if we are in label
        if self.tabs.tab(self.tabs.select(), "text") == LABEL_NAME:
            if event.keysym == KEY_NEXT_PHOTO:
                self.second_tab.next_photo()
            elif event.keysym == KEY_LAST_PHOTO:
                self.second_tab.last_photo()
            elif event.keysym == KEY_DEL_PHOTO:
                self.second_tab.del_photo()
            elif event.char in KEY_LABEL_CHARS:
                self.second_tab.event_win(event)

    def onKeyRelease(self, event):
        if self.devMode:
            print(YELLOW + 'key release: ' + EOC + event.keysym)
        if event.keysym == KEY_CTRL_L:
            self.l_ctrl_pressed = False;


    def open_options(self):
        self.options_frame = Toplevel()
        self.options_frame.geometry("800x400")
        self.options_frame.title("Options")

        self.options_frame.grid()
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=1)

        paths_frame = Frame(self.options_frame)
        paths_frame.grid(row=0, column=0, sticky='new')
        paths_frame.grid_columnconfigure(0, weight=1)
        paths_frame.grid_columnconfigure(1, weight=1)
        paths_frame.grid_columnconfigure(2, weight=1)
        paths_frame.grid_columnconfigure(3, weight=1)
        paths_frame.grid_rowconfigure(0, weight=1)
        paths_frame.grid_rowconfigure(1, weight=1)

        path1_label = Label(paths_frame)
        path1_label.config(text='Photos :', font=("Helvetica", 16))
        path1_label.grid(row=0, column=0, sticky='we')
        self.path1_result = Entry(paths_frame, width=35, font=("Helvetica", 12), justify=CENTER)
        self.path1_result.insert(END, self.cfg.get('paths', 'snap_path'))
        self.path1_result.grid(row=0, column=1, columnspan=2, sticky='we')
        path1_button = Button(paths_frame)
        path1_button.config(image=self.dir_photos_pic, font=("Helvetica", 14), command=self.get_IN_Folder)
        path1_button.grid(row=0, column=3, padx=10, pady=10)

        path2_label = Label(paths_frame)
        path2_label.config(text='Datasets :', font=("Helvetica", 16))
        path2_label.grid(row=1, column=0, sticky='we')
        self.path2_result = Entry(paths_frame, width=35, font=("Helvetica", 12), justify=CENTER)
        self.path2_result.insert(END, self.cfg.get('paths', 'out_path'))
        self.path2_result.grid(row=1, column=1, columnspan=2, sticky='we')
        path2_button = Button(paths_frame)
        path2_button.config(image=self.dir_open_pic, font=("Helvetica", 14), command=self.get_OUT_Folder)
        path2_button.grid(row=1, column=3, padx=10, pady=10)

        handler = lambda: self.close_options(self.options_frame)
        btn = Button(self.options_frame, image=self.save_pic, font=("Helvetica", 16), command=handler)
        btn.grid(row=2, column=0)

    def get_IN_Folder(self):
        IN_path = askdirectory()
        self.options_frame.focus_set()
        if len(IN_path) != 0:
            self.path1_result.delete(0, END)
            self.path1_result.insert(END, IN_path)

    def get_OUT_Folder(self):
        OUT_path = askdirectory()
        self.options_frame.focus_set()
        if len(OUT_path) != 0:
            self.path2_result.delete(0, END)
            self.path2_result.insert(END, OUT_path)


    def close_options(self, options_frame):
        self.IN_path = self.path1_result.get()
        self.OUT_path = self.path2_result.get()
        self.cfg.set('paths', 'out_path', self.OUT_path)
        self.cfg.set('paths', 'snap_path', self.IN_path)
        self.snap_path.set(self.IN_path)
        self.out_path.set(self.OUT_path)
        self.second_tab.load()

        with open(FILE_CONFIG, 'w') as f:
            self.cfg.write(f)

        if options_frame:
            options_frame.destroy()

    def on_Quit(self):
        ret = 0
        ret += self.first_tab.on_quit()
        ret += self.third_tab.on_quit()
        ret += self.fourth_tab.on_quit()
        ret += self.fifth_tab.on_quit()
        if ret == 4:
            self.quit()
