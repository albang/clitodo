#!/usr/bin/env python
from clitodo import View
from todo import Tache, Tag
from menu import TacheMenu, TagMenu, MultiMenu, MagicIndex, TacheTagMenu
import curses
import logging
from datetime import datetime


class Controler(object):

    def __init__(self):
        self.myWindow = View()
        self.menus = []
        self.mIndex = MagicIndex(0)

        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        tagToHide = []
        Tag.hidedTag.append(Tag().ajouter(name="Archive"))

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
        tagMenu = TagMenu(items=Tag().get_tags())
        self.tagMenu = tagMenu
        tagMenu.setTopX(self.myWindow.getMaxXY()["x"]-36)
        self.addMenu(TacheMenu(items=Tache().get_tache_to_show()))
        self.addMenu(tagMenu)
        self.packMenu()
        self.myWindow.main_window(self.menus)
        while True:
            event = self.myWindow.screen.getch()
            if event == ord("Q"):
                self.myWindow.stop()
                exit(0)
            elif event == curses.KEY_DOWN:
                if self.menus[self.mIndex.getCurrent()].moveDown():
                    self.myWindow.redraw_menu(self.currentMenu)
            elif event == curses.KEY_UP:
                if self.menus[self.mIndex.getCurrent()].moveUp():
                    self.myWindow.redraw_menu(self.currentMenu)
            elif event == curses.KEY_RIGHT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.myWindow.redraw_menu(self.currentMenu)
                self.menus[self.mIndex.goNext()].selection()
                self.myWindow.redraw_menu(self.currentMenu)
                #self.myWindow.main_window(self.menus)
            elif event == curses.KEY_LEFT:
                self.menus[self.mIndex.getCurrent()].noSelection()
                self.myWindow.redraw_menu(self.currentMenu)
                self.menus[self.mIndex.goPrevious()].selection()
                self.myWindow.redraw_menu(self.currentMenu)
                #self.myWindow.main_window(self.menus)
            elif event == ord("A"):
                newTache = self.myWindow.print_ajouter_tache()
                Tache().ajouter_tache(newTache, datetime.now())
            elif event == ord("G"):
                newTache = self.myWindow.print_ajouter_tag()
                Tache().ajouter_tache()
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
                tagMenu = TagMenu(items=Tag().get_tags())
                tagMenu.setTopX(self.myWindow.getMaxXY()["x"]-36)
                self.addMenu(TacheMenu(items=Tache().get_tache_to_show()))
                self.addMenu(tagMenu)
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
                self.myWindow.redraw_menu(menu)
            elif event == curses.KEY_UP:
                menu.moveUp()
                self.myWindow.redraw_menu(menu)
            elif event == 10:  # enter key
                retour=menu.performAction()
                if retour == "AddTag":
                    newTag=self.myWindow.print_ajouter_tag(self.tagMenu)
                    Tag().ajouter(newTag)
                    self.tagMenu.reload(Tag().get_tags())
                menu.noSelection()
                break


if __name__ == '__main__':
    myApplication = Controler()
    myApplication.start()
