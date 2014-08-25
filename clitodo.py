#!/usr/bin/env python
import curses
from todo import Tache, Tag
from curses.textpad import Textbox, rectangle
from menu import MultiMenu
import logging

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
        #log.redraw_menu(ging.basicConfig(filename='example.log', level=#logging.DEBUG)
        ##logging.basicConfig(filename='info.log', level=#logging.INFO)

    def stop(self):
        curses.endwin()

    def main_window(self, menus):
        self.screen.clear()
        self.print_rectangle(99, 0, 115, 6)
        self.print_rectangle(2, 0, 96, 20)
        for menu in menus:

            self.print_menu(menu)
        self.print_bottom_msg()

    def print_menu(self, menu):
        #logging.debug("print menu >"+menu.title)
        if type(MultiMenu([])) == type(menu):
            tX, tY, dX, dY = menu.entoureMe()
            self.print_rectangle(tX, tY, dX, dY)
        ##logging.debug("[print_menu] nb_item" + str(menu.menuLength))
        self.screen.addstr(menu.topY, menu.topX, menu.title)
        ##logging.info("[print_menu] Type menu.items" + str(type(menu.items)))
        #pprint(menu.items)
        for indice, item in enumerate(list(menu.items)):
        #for indice, item in menu.items.items:
         #   #logging.info("[print_menu]" + str(item) + " indice "+str(indice))
            self.print_item(menu, item, indice)

    def print_item(self, menu, item, index):
        cleanStr = (menu.maxItemWidth - len(str(item)))*" "
        ##logging.debug("[print_item] item "+str(index))
        if menu.isSelected(index):
            self.screen.addstr(menu.firstItemY + index,
                               menu.firstItemX,
                               menu.selector + str(item),
                               curses.A_STANDOUT
                               )
            if len(cleanStr) > 0:
                endLine = menu.firstItemX + len(menu.selector) + len(str(item))
                self.screen.addstr(menu.firstItemY + index, endLine, cleanStr)
        else:
            self.screen.addstr(menu.firstItemY + index,
                               menu.firstItemX,
                               len(menu.selector)*" " + str(item)+cleanStr)

        self.screen.refresh()

    def redraw_menu(self, menu):
        self.screen.addstr(menu.firstItemY + menu.getSelectedIndex(),
                           menu.firstItemX,
                           menu.selector + str(menu.getSelected()),
                           curses.A_STANDOUT
                           )
            #if len(cleanStr) > 0:
            #    endLine = menu.firstItemX + len(menu.selector) + len(str(item))
            #    self.screen.addstr(menu.firstItemY + index, endLine, cleanStr)
        self.screen.addstr(menu.firstItemY + menu.getPreviousIndex(),
                           menu.firstItemX,
                           len(menu.selector)*" " + str(menu.getPrevious()))

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

    def print_bottom_msg(self):
        bottom_menu = ("A for Add;" +
                       "Q For Quit;" +
                       "T for To do;" +
                       "D for Done;" +
                       "F for Flash;" +
                       "S for Supress"
                       )
        if len(bottom_menu) > self.max["x"]:
            self.screen.addstr(self.max["y"] - 1,
                               1, "NO MENU", curses.A_STANDOUT)
        else:
            self.screen.addstr(self.max["y"]-1,
                               2, bottom_menu, curses.A_STANDOUT)