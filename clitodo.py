#!/usr/bin/env python
import curses


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

    def stop(self):
        curses.endwin()

    def main_window(self, menus):
        for menu in menus:
            self.print_menu(menu)

    def print_menu(self, menu):
        self.screen.addstr(menu.topY, menu.topX, menu.title)
        for indice, item in enumerate(menu.items):
            self.print_item(menu, item, indice)

    def print_item(self, menu, item, index):
        if menu.isSelected(index):
            self.screen.addstr(menu.topY + 1 + index,
                               menu.topX + menu.padding,
                               menu.selector + item.stringmoica(),
                               curses.A_STANDOUT
                               )
        else:
            self.screen.addstr(menu.topY + 1 + index,
                               menu.topX + menu.padding,
                               len(menu.selector)*" " + item.stringmoica()
                               )

    def print_tags(ecran, x, y, tache):
        ltTags = tache.get_tags()
        if len(ltTags) > 0:
            i = 0
            for tag in ltTags:
                screen.addstr(y, x+i, " ")
                screen.addstr(y, x+i, tag.name, curses.color_pair(1))
                i = len(tag.name) + 1
