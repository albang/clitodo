#!/usr/bin/env python
from clitodo import View
from todo import Tache, Tag
from menu import Menu, TagMenu, MagicIndex
import curses


class Controler(object):

    def __init__(self):
        self.myWindow = View()
        self.menus = []
        self.currentMenu = 0
        self.mIndex = MagicIndex(0)

    def addMenu(self, menu):
        self.menus.append(menu)
        self.mIndex.maxLimit = len(self.menus)

    def packMenu(self):
        for indice in xrange(1, len(self.menus)):
            self.menus[indice].noSelection()

    def start(self):

        self.addMenu(Menu(items=Tache().get_tache_undone()))
        self.addMenu(TagMenu(items=Tag().get_tags()))
        self.packMenu()
        self.myWindow.main_window(self.menus)
        while True:
            event = self.myWindow.screen.getch()
            if event == ord("Q"):
                self.myWindow.stop()
                exit(0)
            if event == curses.KEY_DOWN:
                self.menus[self.mIndex.getCurrent()].moveDown()
                self.myWindow.main_window(self.menus)
            if event == curses.KEY_UP:
                self.menus[self.mIndex.getCurrent()].moveUp()
                self.myWindow.main_window(self.menus)
            if event == curses.KEY_RIGHT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.menus[self.mIndex.next()].selection()
                self.myWindow.main_window(self.menus)
            if event == curses.KEY_LEFT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.menus[self.mIndex.previous()].selection()
                self.myWindow.main_window(self.menus)
if __name__ == '__main__':
    myApplication = Controler()
    myApplication.start()
