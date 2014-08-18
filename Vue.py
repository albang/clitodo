#!/usr/bin/env python

from todo import Tache
from datetime import datetime
import curses
from curses.textpad import Textbox, rectangle


def print_bottom_menu(ecran):
    taille_screen = ecran.getmaxyx()
    print_notification(ecran, str(taille_screen)+"     ")
    bottom_menu = ("A pour Ajouter;" +
                   "Q For Quit;" +
                   "T for To do;" +
                   "D for Done;" +
                   "F for Flash"
                   )

    if len(bottom_menu) > taille_screen[1]:
        ecran.addstr(taille_screen[0]-1, 1, "NO MENU", curses.A_STANDOUT)
    else:
        ecran.addstr(taille_screen[0]-1, 1, bottom_menu, curses.A_STANDOUT)

     #ecran.addstr(str(taille_screen[0]))


def print_title(ecran):
    ecran.addstr("Bienvenue dans la todo\n", curses.A_STANDOUT)


def print_notification(ecran, message):
    taille_screen = ecran.getmaxyx()
    ecran.addstr(0, taille_screen[1]-len(message), message, curses.A_STANDOUT)


def print_main_screen(ecran):
    print_title(ecran)
    print_bottom_menu(ecran)


def print_taches(ecran, taches, message):
    ecran.addstr(2, 2, message+"\n")
    for tache in taches:
        #ecran.addstr(get_pos(ecran)["y"]+1, 4,
        #             str(tache.date_creation)+" "+tache.description)
        print_tache(ecran, 3, get_pos(ecran)["y"]+1, tache)


def print_tache(ecran, x, y, tache, isSelected=False):
    lsTache = tache.stringmoica(isSelected)
    if isSelected is True:
        screen.addstr(y, x, lsTache, curses.A_REVERSE)
    else:
        screen.addstr(y, x, lsTache)
    print_tags(ecran, x + len(lsTache) + 1, y, tache)


def print_tags(ecran, x, y, tache):
    ltTags = tache.get_tags()    
    if len(ltTags) > 0:
        for tag in ltTags:
            screen.addstr(y, x, " "+tag.name, curses.color_pair(1))


def get_pos(ecran):
    dico = {}
    dico["x"] = ecran.getyx()[1]
    dico["y"] = ecran.getyx()[0]
    return(dico)


def window_for_done_task(screen):
    screen.clear()
    print_taches(screen, Tache().get_tache_done(), "Taches faites")
    print_bottom_menu(screen)
    #A voir si on ne peut pas recuperer ca en code
    deal_with_selected(screen, 33, 45, Tache().get_tache_done(),
                       window_for_done_task)


def window_for_undone_task(screen):
    screen.clear()
    print_taches(screen, Tache().get_tache_undone(), "Taches a faire :")
    print_bottom_menu(screen)
    deal_with_selected(screen, 33, 45, Tache().get_tache_undone(),
                       window_for_undone_task)


def main_control(screen, event, inception_level):
    if event == ord("Q"):
        curses.endwin()
        exit(0)
    if event == ord("D"):
        window_for_done_task(screen)
    if event == ord("T"):
        window_for_undone_task(screen)
    if event == ord("F"):
        curses.flash()
    if event == ord("A"):
        editwin = curses.newwin(1,
                                screen.getmaxyx()[1]-6,
                                screen.getmaxyx()[0]-4,
                                1
                                )
        rectangle(screen,
                  screen.getmaxyx()[0]-5,
                  0, screen.getmaxyx()[0]-3,
                  screen.getmaxyx()[1]-5)
        screen.refresh()
        box = Textbox(editwin)
        # Let the user edit until Ctrl-G is struck.
        box.edit()
        # Get resulting contents
        message = box.gather()
        Tache().ajouter_tache(message, datetime.now())
        screen.clear()
        print_main_screen(screen)
        print_taches(screen, Tache().get_tache_undone(), "Taches a faire :")
        deal_with_selected(screen, 33, 45, Tache().get_tache_undone(),
                           window_for_undone_task)


def deal_with_selected(screen, x, y, taches, parent_function):
    nb_taches = taches.count()
    if nb_taches > 0:
        #initisation,on selectionne la premiere tache
        print_tache(screen, 3, 4,taches[0], True)
        i = 0   
    else:
        i = 0
        screen.addstr(4, 3, " " + "rien a afficher",
                                  curses.A_REVERSE)

    while True:
        event = screen.getch()
        if nb_taches > 0:
            if event == curses.KEY_DOWN:
                i = i + 1
                i %= taches.count()
                print_notification(screen,
                                   " "+str(i)+"   [" +
                                   str(Tache().count_tache_undone()) +
                                   "/" + str(Tache().count_tache_done())+"]"
                                   )
                if i == 0:
                    print_tache(screen, 3, 4 + taches.count() - 1,
                                taches[taches.count() - 1])
                    print_tache(screen, 3, 4 + i, taches[i], True)
                else:
                    print_tache(screen, 3, 4 + i - 1, taches[i-1])
                    print_tache(screen, 3, 4 + i, taches[i], True)
            if event == curses.KEY_UP:
                i = i - 1
                print_notification(screen,
                                   " " +
                                   str(i) +
                                   " [" +
                                   str(Tache().count_tache_undone()) +
                                   "/" +
                                   str(Tache().count_tache_done()) +
                                   "]"
                                   )
                if i < 0:
                    print_tache(screen, 3, 4, taches[0])
                    i = taches.count()-1
                    print_tache(screen, 3, 4 + i, taches[i], True)
                else:
                    print_tache(screen, 3, 4 + i + 1, taches[i + 1])
                    print_tache(screen, 3, 4 + i, taches[i], True)

            if event == ord("P"):
                if i >= 0:
                    taches[i].change_status()
                    parent_function(screen)
                    print_notification(screen,
                                       " "+str(type(parent_function))
                                       )
            if event == ord("S"):
                if i >= 0:
                    taches[i].delete2()
                    parent_function(screen)
                    print_notification(screen,
                                       " "+str(type(parent_function))
                                       )
        main_control(screen, event, 1)


screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
print_main_screen(screen)
print_notification(screen,
                   "[" + str(Tache().count_tache_undone()) +
                   "/" + str(Tache().count_tache_done())+"]"
                   )


while True:
    event = screen.getch()
    main_control(screen, event, 0)
curses.endwin()
