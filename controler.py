#!/usr/bin/env python
from clitodo import View
from todo import Tache, Tag
from menu import Menu, TagMenu, MultiMenu, MagicIndex
import curses
import logging

class Controler(object):

    def __init__(self):
        self.myWindow = View()
        self.menus = []
        self.mIndex = MagicIndex(0)
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def addMenu(self, menu):
        self.menus.append(menu)
        self.mIndex.maxLimit = len(self.menus)

    def packMenu(self):
        for indice in range(1, len(self.menus)):
            self.menus[indice].noSelection()

    @property
    def currentMenu(self):
        return(self.menus[self.mIndex.getCurrent()])

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
            elif event == curses.KEY_DOWN:
                self.menus[self.mIndex.getCurrent()].moveDown()
                self.myWindow.main_window(self.menus)
            elif event == curses.KEY_UP:
                self.menus[self.mIndex.getCurrent()].moveUp()
                self.myWindow.main_window(self.menus)
            elif event == curses.KEY_RIGHT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.menus[self.mIndex.next()].selection()
                self.myWindow.main_window(self.menus)
            elif event == curses.KEY_LEFT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.menus[self.mIndex.previous()].selection()
                self.myWindow.main_window(self.menus)
            if event == 10: # enter key 
                logging.debug("Enter PRessed")
                x,y = self.currentMenu.getSelectedPosition()
                actionMenu = MultiMenu(self.currentMenu.getSelected().getAction(),x+ self.currentMenu.getItemLength() ,y)
                logging.debug(str(actionMenu.menuLength))
                x, y =actionMenu.getSelectedPosition()
                self.myWindow.screen.addstr("==>")
                self.myWindow.print_menu(actionMenu)
if __name__ == '__main__':
    myApplication = Controler()
    myApplication.start()
