#!/usr/bin/env python
import curses
from todo import Tache, Tag
from curses.textpad import Textbox, rectangle


class View(object):
    screen = ""
    menu = {}
    #main_menu = {"Ajouter une tache": self.controler.add_task,
    #             "Voir taches": self.controler.show_task,
    #             "supprimer tache": self.controler.del_task
    #             }
    #tags_menu = Controler.getTagMenu()
    #current_window= fenetre_principale

    def __init__(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.max = {}
        self.max["y"], self.max["x"] = self.screen.getmaxyx()
        Tag().init_renderer()
        Tache().init_renderer()

    def stop(self):
        curses.endwin()

    def main_window(self, menus):
        self.print_rectangle(99, 0, 115, 6)
        self.print_rectangle(2, 0, 96, 20)
        for menu in menus:
            self.print_menu(menu)
        self.print_bottom_msg()

    def print_menu(self, menu):
        self.screen.addstr(menu.topY, menu.topX, menu.title)
        for indice, item in enumerate(menu.items):
            self.print_item(menu, item, indice)

    def print_bottom_msg(self):
        bottom_menu = ("A for Add;" +
                       "Q For Quit;" +
                       "T for To do;" +
                       "D for Done;" +
                       "F for Flash;" +
                       "S for Supress"
                       )

        if len(bottom_menu) > self.max["x"]:
            self.screenQ.addstr(self.max["y"] - 1, 1, "NO MENU", curses.A_STANDOUT)
        else:
            self.screen.addstr(self.max["y"]-1, 2, bottom_menu, curses.A_STANDOUT)


    def print_item(self, menu, item, index):
        if menu.isSelected(index):
            self.screen.addstr(menu.topY + 1 + index,
                               menu.topX + menu.padding,
                               menu.selector + str(item),
                               curses.A_STANDOUT
                               )
        else:
            self.screen.addstr(menu.topY + 1 + index,
                               menu.topX + menu.padding,
                               len(menu.selector)*" " + str(item)
                               )

    def print_tags(ecran, x, y, tache):
        ltTags = tache.get_tags()
        if len(ltTags) > 0:
            i = 0
            for tag in ltTags:
                ecran.addstr(y, x + i, " ")
                ecran.addstr(y, x + i, tag.name, curses.color_pair(1))
                i = len(tag.name) + 1

    def print_rectangle(self, tlX, tlY, drX, drY):
        rectangle(self.screen, tlY, tlX, drY, drX)
        self.screen.refresh()
