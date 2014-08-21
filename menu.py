#!/usr/bin/env python


class Menu(object):
    """docstring for Menu"""
    title = "Menu"
    topX = 4
    topY = 0
    padding = 2
    menuLength = 0
    maxItemWidth = 0
    selectedIndex = 0
    previousIndex = -1
    selector = "===>"
    items = ""

    def __init__(self, items, title="Menu"):
        super(Menu, self).__init__()
        self.items = items
        self.menuLength = items.count()

    def moveUp(self):
        self.previousIndex = self.selectedIndex
        self.selectedIndex -= 1
        if self.selectedIndex < 0:
            self.selectedIndex = self.menuLength - 1

    def moveDown(self):
        self.previousIndex = self.selectedIndex
        self.selectedIndex += 1
        self.selectedIndex %= self.menuLength

    def moveLeft(self):
        pass

    def moveRigt(self):
        pass

    def isSelected(self, index):
            return(index == self.selectedIndex)

    def noSelection(self):
        self.selectedIndex = -1

    def selection(self, index=0):
        self.selectedIndex = index


class TagMenu(Menu):
    """docstring for TagMenu"""
    def __init__(self, items, title="Tags"):
        super(Menu, self).__init__()
        self.items = items
        self.menuLength = items.count()
        self.title = title
        self.topX = 100


class MagicIndex(object):
    """docstring for MagicIndex"""
    def __init__(self, maxLimit, current=0):
        super(MagicIndex, self).__init__()
        self.maxLimit = maxLimit
        self.current = current

    def next(self):
        self.current += 1
        self.current %= self.maxLimit
        return(self.current)

    def previous(self):
        self.current -= 1
        if self.current < 0:
            self.current = self.maxLimit - 1
        return(self.current)

    def getCurrent(self):
        return(self.current)
