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
        tagToHide = []

    def addMenu(self, menu):
        self.menus.append(menu)
        self.mIndex.maxLimit = len(self.menus)

    def clearMenu(self):
        self.menus = []
        self.mIndex.setCurrent(0)

    def packMenu(self):
        #pas correct
        #logging.debug("[pack_menu] taille liste"+str(len(self.menus)))
        self.menus[0].selection(0)
        #logging.debug("[pack_menu] reset du premier menu a" +
        #                str(self.menus[0].getSelectedIndex()))
        for indice in range(1, len(self.menus)):
            self.menus[indice].noSelection()

    @property
    def currentMenu(self):
        logging.info("[current]Curent menu " +
                     str(self.menus[self.mIndex.getCurrent()]))
        return(self.menus[self.mIndex.getCurrent()])

    def start(self):

        self.addMenu(Menu(items=Tache().get_tache_to_show()))
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
                self.myWindow.redraw_menu(self.currentMenu)
            elif event == curses.KEY_UP:
                self.menus[self.mIndex.getCurrent()].moveUp()
                self.myWindow.main_window(self.menus)
                self.myWindow.redraw_menu(self.currentMenu)
            elif event == curses.KEY_RIGHT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.menus[self.mIndex.next()].selection()
                self.myWindow.main_window(self.menus)
            elif event == curses.KEY_LEFT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.menus[self.mIndex.previous()].selection()
                self.myWindow.main_window(self.menus)
            elif event == 10:  # enter key
                logging.debug("Enter Pressed")
                x, y = self.currentMenu.getSelectedPosition()
                actionList = self.currentMenu.getSelected().getAction()
                itemLength = self.currentMenu.getItemLength()
                actionMenu = MultiMenu(actionList, x + itemLength, y, "=>")
                logging.debug(str(actionMenu.menuLength))
                x, y = actionMenu.getSelectedPosition()
                self.myWindow.print_menu(actionMenu)
                self.popUpMenu(actionMenu)
                self.clearMenu()
                self.addMenu(Menu(items=Tache().get_tache_to_show()))
                self.addMenu(TagMenu(items=Tag().get_tags()))
                self.packMenu()
                self.myWindow.main_window(self.menus)

    def popUpMenu(self, menu):
        while True:
            event = self.myWindow.screen.getch()
            if event == ord("Q"):
                self.myWindow.stop()
                exit(0)
            if event == curses.KEY_DOWN:
                menu.moveDown()
                self.myWindow.print_menu(menu)
            elif event == curses.KEY_UP:
                menu.moveUp()
                self.myWindow.print_menu(menu)
            elif event == 10:  # enter key
                menu.performAction()
                menu.noSelection()
                break


if __name__ == '__main__':
    myApplication = Controler()
    myApplication.start()
