# -*- coding: utf-8 -*-

from srcs.const import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText

import os
import configparser
from time import time, localtime, strftime, sleep

from PIL import ImageTk, Image

import srcs.Tk_Tooltips as ttp

"""
labelisation
"""

class SecondTab(object):

    def __init__(self, app):
        self.app = app
        self.label_frame = Frame(app.second_tab)
        self.label_frame.grid(row=0, column=0, stick='n')
        self.label_frame.grid_columnconfigure(0, weight=1)
        self.label_frame.grid_rowconfigure(0, weight=1)

        self.fen = {
            'fen' : None,
            'lab_photo' : None,
            'photo' : None,
            'lab_info' : None
        }
        self.fen['fen'] = Frame(self.label_frame,
                width=WIDTH_IMG, height=HEIGHT_IMG)
        self.fen['fen'].grid(row=0, column=0, sticky='n')


        self.command_frame = Frame(self.label_frame)
        self.command_frame.grid(row=1, column=0, sticky='n')
        self.command_frame.grid_columnconfigure(0, weight=1)
        self.command_frame.grid_columnconfigure(1, weight=1)
        self.command_frame.grid_columnconfigure(2, weight=1)
        self.command_frame.grid_columnconfigure(3, weight=1)
        self.command_frame.grid_columnconfigure(4, weight=1)
        self.command_frame.grid_columnconfigure(5, weight=1)
        self.command_frame.grid_rowconfigure(0, weight=1)

        load_handler = lambda: self.load(self)

        self.reload_pic = ImageTk.PhotoImage(Image.open('assets/reload.png'))

        self.reload_but = Button(self.command_frame)
        self.reload_but.config(image=self.reload_pic, command=load_handler)
        self.reload_but.grid(row=0, column=0, padx=10)
        reload_ttp = ttp.ToolTip(self.reload_but, 'Reload labelisation',
                msgFunc=None, delay=1, follow=True)

        self.dir_srcs = None  # directory with photos
        self.dir_dest = None  # directory with labelised photos
        self.photos = None    # list with all photos
        self.auto_next = True # go automatically to next photo

        self.load()


    def load(self, event=None):
        self.dir_srcs = self.app.cfg.get('paths', 'snap_path')
        if self.dir_srcs != '' and self.dir_srcs[-1] != '/':
            self.dir_srcs += '/'
        self.dir_dest = self.app.cfg.get('paths', 'out_path')
        if self.dir_dest != '' and self.dir_dest[-1] != '/':
            self.dir_dest += '/'
        try:
            self.photos = os.listdir(self.dir_srcs)
        except FileNotFoundError:
            self.photos = []
        self.photo_act = 0
        if len(self.photos) == 0:
            return

        for i in range(len(self.photos) - 1, -1, -1):
            remove = 1
            for ext in EXT_PHOTOS:
                if len(self.photos[i]) > len(ext) and self.photos[i][-len(ext):] == ext:
                    remove = 0
                    break
            if remove == 1:
                self.photos.pop(i)
            else:
                self.photos[i] = self.dir_srcs + self.photos[i]
        self.print_win()



    def print_win(self):
        if len(self.photos) == 0:
            return
        if self.fen['lab_photo'] != None:
            self.fen['lab_photo'].destroy()
        if self.fen['lab_info'] != None:
            self.fen['lab_info'].destroy()
        image = Image.open(self.photos[self.photo_act])
        image = image.resize((WIDTH_IMG, HEIGHT_IMG - 50), Image.ANTIALIAS)
        self.fen['photo'] = ImageTk.PhotoImage(image)
        self.fen['lab_photo'] = Label(self.fen['fen'], image=self.fen['photo'])
        self.fen['lab_photo'].pack(side=TOP)
        self.fen['lab_info'] = Label(self.fen['fen'], width=32, height=2, font=("Courier", 40))
        self.fen['lab_info']['text'] = self.get_label() + '\t\t' + str(self.photo_act) + '/' + str(len(self.photos))
        self.fen['lab_info'].pack(side=BOTTOM)


    def last_photo(self):
        if len(self.photos) == 0:
            return
        self.photo_act -= 1
        if self.photo_act < 0:
            self.photo_act = len(self.photos) - 1
        self.print_win()

    def next_photo(self):
        if len(self.photos) == 0:
            return
        self.photo_act += 1
        if self.photo_act >= len(self.photos):
            self.photo_act = 0
        self.print_win()


    def event_win(self, event):
        if len(self.photos) == 0:
            return
        self.set_label(event.char)
        if self.auto_next == True:
            self.next_photo()
        else:
            self.print_win()


    def set_label(self, label):
        if len(self.photos) == 0:
            return
        new = self.dir_dest
        if self.get_label() == '':
            if self.photos[self.photo_act].split('/')[-1][0] == '_':
                new += label + self.photos[self.photo_act].split('/')[-1]
            else:
                new += label + '_' + self.photos[self.photo_act].split('/')[-1]
        else:
            new += label + '_' + self.photos[self.photo_act].split('/')[-1].split('_')[1:][0]
        print(GREEN + 'RENAME: ' + EOC + new)
        os.rename(self.photos[self.photo_act], new)
        self.photos[self.photo_act] = new


    def get_label(self):
        if len(self.photos) == 0:
            return
        try:
            char = self.photos[self.photo_act].split('/')[-1].split('_')[0]
            if len(char) == 1 and char.isdigit():
                return char
        except:
            pass
        return ''


    def del_photo(self):
        if len(self.photos) == 0:
            return
        print(RED + 'REMOVE: ' + EOC + self.photos[self.photo_act])
        os.remove(self.photos[self.photo_act])
        self.photos.pop(self.photo_act)
        if self.photo_act >= len(self.photos):
            self.photo_act = 0
        self.print_win()
