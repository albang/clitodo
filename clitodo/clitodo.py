#!/usr/bin/env python
import curses
from todo import Tache, Tag
from curses.textpad import Textbox, rectangle
from menu import TacheMenu, TagMenu, MultiMenu, TacheTagMenu
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
        curses.use_default_colors()
        #curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.max = {}
        self.max["y"], self.max["x"] = self.screen.getmaxyx()
        Tag().init_renderer()
        Tache().init_renderer()
        #log.redraw_menu(ging.basicConfig(filename='example.log', level=#logging.DEBUG)
        ##logging.basicConfig(filename='info.log', level=#logging.INFO)
        cpt = 0
        for i in range(-1, 8):
            for y in range(-1, 8):
                curses.init_pair(cpt, y, i)
                cpt += 1

    def getMaxXY(self):
        """
            This funtion return Max x y coordinate of the terminal screen
            :returns: a dictionary with "x" and "y" 
        """
        return(self.max)

    def stop(self):
        """
            This function quit cleanly the terminal.
        """
        curses.endwin()

    def main_window(self, menus):
        """
            This function print a list of menus
            Perhaps we can change the name because nothing is hardcoded
            maybe print_windows
            :param menus:memus
            :type menu:A list of Menu
            :returns: None
        """
        self.screen.clear()
        for menu in menus:

            self.print_menu(menu)
        self.print_bottom_msg()

    def print_menu(self, menu):
        """
            This is a "meta" function which print a menu
            :param menu:menu
            :type menu: Menu
        """
        #logging.debug("print menu >"+menu.title)
        if type(MultiMenu([])) == type(menu):
            self.print_action_menu(menu)
        elif isinstance(menu, TacheMenu):
            self.print_tache_menu(menu)
        elif isinstance(menu, TagMenu):
            self.print_tag_menu(menu)

    def print_tache_menu(self, menu):
        """
            This is a "meta" function which print a menu
            :param menu:menu
            :type menu: Menu
        """
        tX, tY, dX, dY = menu.entoureMe()
        # + 12t o be patched :
        # Probleme : tg length
        self.print_rectangle(tX, tY, dX + 12, dY)
        self.screen.addstr(menu.topY, menu.topX, menu.title)
        for indice, item in enumerate(list(menu.items)):
            self.print_item(menu, item, indice)
            tagsMenus = menu.getSubMenu()
            self.print_tacheTagMenu(tagsMenus[indice])
            #self.print_item(menu.getSubMenu()[indice], item, indice)

    def print_tacheTagMenu(self, tacheTagMenu):
        if tacheTagMenu.getMenuLength() > 0:
            i = 0
            for item in tacheTagMenu.getItems():
                self.screen.addstr(tacheTagMenu.getFirstItemY() + i,
                                   tacheTagMenu.getFirstItemX(), " ")
                x, y = tacheTagMenu.getItemPosition(i)
                if i == tacheTagMenu.getSelectedIndex():
                    self.screen.addstr(y, x, ">"+item.name,
                                       curses.color_pair(13)
                                       )
                else:
                    self.screen.addstr(y, x, " ")
                    self.screen.addstr(y,
                                       x+1,
                                       item.name,
                                       curses.color_pair(13)
                                       )
                i += 1

    def print_tag_menu(self, menu):
        self.screen.addstr(menu.topY, menu.topX, menu.title)
        tX, tY, dX, dY = menu.entoureMe()
        self.print_rectangle(tX, tY, dX + 12, dY)
        for indice, item in enumerate(list(menu.items)):
            self.print_item(menu, item, indice)

    def print_action_menu(self, menu):
        tX, tY, dX, dY = menu.entoureMe()
        #logging.INFO("print_action_menu Max X" + self.getMaxXY()["x"] +
        #             " Max Y"+self.getMaxXY()["y"])
        logging.info("print_action_menu :" +
                     " Top x " + str(tX) +
                     " Top Y" + str(tY) +
                     " Down X" + str(dX) +
                     " Down Y" + str(dY) +
                     " Max Y"+str(self.getMaxXY()["y"]))
        #si le bas du rectangle deplace la fenetre
        if dY >= self.getMaxXY()["y"]:
            tY = tY - (dY - self.getMaxXY()["y"] + 1)
            dY = dY - (dY - self.getMaxXY()["y"] + 1)
            menu.setTopY(tY)
        logging.info("print_action_menu :" +
                     " Top x " + str(tX) +
                     " Top Y" + str(tY) +
                     " Down X" + str(dX) +
                     " Down Y" + str(dY) +
                     " Max Y"+str(self.getMaxXY()["y"]))
        self.print_rectangle(tX, tY, dX, dY)
        self.screen.addstr(menu.topY, menu.topX, menu.getTitle())
        for indice, item in enumerate(list(menu.items)):
            self.print_item(menu, item, indice)

    def print_item(self, menu, item, index):
        cleanStr = (menu.maxItemWidth - len(str(item)))*" "
        # logging.debug("[print_item] item "+str(index))
        x, y = menu.getItemPosition(index)
        if menu.isSelected(index):
            self.screen.addstr(y, x, menu.getSelector() + str(item),
                               curses.A_STANDOUT
                               )
        else:
            self.screen.addstr(y, x, len(menu.getSelector())*" " + str(item))
        if len(cleanStr) > 0:
                endLine = menu.firstItemX +\
                          len(menu.getSelector()) +\
                          len(str(item))
                self.screen.addstr(menu.firstItemY + index,
                                   endLine,
                                   cleanStr,
                                   curses.color_pair(1)
                                   )

        self.screen.refresh()

    def redraw_menu(self, menu):
        if menu.getSelectedIndex() >= 0:
            self.screen.addstr(menu.firstItemY + menu.getSelectedIndex(),
                               menu.firstItemX,
                               menu.getSelector() + str(menu.getSelected()),
                               curses.A_STANDOUT
                               )
            # if len(cleanStr) > 0:
            #    endLine = menu.firstItemX + len(menu.getSelector()) + len(str(item))
            #    self.screen.addstr(menu.firstItemY + index, endLine, cleanStr)
        if menu.getPreviousIndex() >= 0:
            self.screen.addstr(menu.firstItemY + menu.getPreviousIndex(),
                               menu.firstItemX,
                               len(menu.getSelector())*" " +
                               str(menu.getPrevious()))

    def print_tags(ecran, x, y, tache):
        ltTags = tache.get_tags()
        if len(ltTags) > 0:
            i = 0
            for tag in ltTags:
                ecran.addstr(y, x + i, " ")
                ecran.addstr(y, x + i, tag.name, curses.color_pair(1))
                i = len(tag.name) + 1

    def print_rectangle(self, tlX, tlY, drX, drY):
        logging.info("print_rectangle :" +
                     " Top x " + str(tlX) +
                     " Top Y" + str(tlY) +
                     " Down X" + str(drX) +
                     " Down Y" + str(drY) +
                     " Max Y"+str(self.getMaxXY()["y"]) +
                     " Max X"+str(self.getMaxXY()["x"])
                     )
        try:
            rectangle(self.screen, tlY, tlX, drY, drX)
        except Exception as e:
            logging.info(e)
        self.screen.refresh()

    def print_ajouter_tache(self):
        self.screen.addstr(self.max["y"]-6, 1, "Ajouter une tache :")
        editwin = curses.newwin(1,
                                self.max["x"]-6,
                                self.max["y"]-4,
                                1
                                )
        rectangle(self.screen,
                  self.screen.getmaxyx()[0]-5,
                  0, self.max["y"]-3,
                  self.max["x"]-5)
        self.screen.refresh()
        box = Textbox(editwin)
        # Let the user edit until Ctrl-G is struck.
        box.edit()
        # Get resulting contents
        message = box.gather()
        return(message)

    def print_ajouter_tag(self, tagMenu):
        tagMenu.getLastItemY()
        newTagStr = "New TAG >"
        self.screen.addstr(tagMenu.getLastItemY(),
                           tagMenu.getFirstItemX()+len(tagMenu.getSelector())-len(newTagStr),
                           newTagStr)
        editwin = curses.newwin(
                                1,
                                self.max["x"]-tagMenu.getFirstItemX()+len(tagMenu.getSelector()),
                                tagMenu.getLastItemY(),
                                tagMenu.getFirstItemX()+len(tagMenu.getSelector()),
                                )
        self.screen.refresh()
        box = Textbox(editwin)
        # Let the user edit until Ctrl-G is struck.
        box.edit()
        # Get resulting contents
        message = box.gather()
        return(message)

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