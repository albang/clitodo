#!/usr/bin/env python
import logging

class Menu(object):
    """docstring for Menu"""
    title = "Menu"
    topX = 4
    topY = 0
    padding = 2
    firstItemX = topX + padding
    firstItemY = topY + 1
    menuLength = 0
    selectedIndex = 0
    previousIndex = -1
    selector = "===>"
    items = []
    logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def getMenuLength(self):
        return(self.menuLength)

    def getItems(self):
        return(self.items)

    def moveUp(self):
        logging.debug("[menu]Move up")
        self.previousIndex = self.selectedIndex
        self.selectedIndex -= 1
        if self.selectedIndex < 0:
            self.selectedIndex = self.menuLength - 1

    def moveDown(self):
        logging.debug("[menu]Move down")
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
        logging.debug("[" + self.title + "] noselection index"+str(self.selectedIndex))
        self.previousIndex = self.selectedIndex
        self.selectedIndex = -1

    def selection(self, index=0):
        self.previousIndex = self.selectedIndex
        self.selectedIndex = index
        logging.debug("[" + self.title + "] selection index"+str(self.selectedIndex))

    def getSelected(self):
        logging.info("[menu][GetSelected] " +
                     self.title + " " + str(self.selectedIndex))
        return(self.items[self.selectedIndex])

    def getPrevious(self):
        if self.menuLength > 1:
            logging.info("[menu][GetSelected] " +
                         self.title + " " + str(self.selectedIndex))
            return(self.items[self.previousIndex])

    def getSelectedIndex(self):
        return(self.selectedIndex)

    def getPreviousIndex(self):
        return(self.previousIndex)

    def getSelectedPosition(self):
        return(
               (self.topX + self.padding + len(self.selector)),
               (self.topY + 1 + self.selectedIndex)
               )

    def getItemLength(self):
        return(len(str(self.items[self.selectedIndex])))

    def performAction(self):
        self.action[self.getSelected()]()
        pass

    def setTopX(self, topX):
        self.topX = topX
        self.firstItemX = self.topX + self.padding

    def getTopX(self):
        return(self.topX)

    def setTopY(self, topY):
        self.topY = topY
        self.firstItemY = topY + 1

    def getFirstItemX(self):
        return(self.firstItemX)

    def getFirstItemY(self):
        return(self.firstItemY)

    def getTopY(self):
        return(self.topY)

    @property
    def maxItemWidth(self):
        maxWidth = 0
        for item in self.items:
            if len(str(item)) > maxWidth:
                maxWidth = (len(str(item)))
        return(maxWidth)

    def entoureMe(self):
        tX = self.firstItemX - len(self.selector)
        tY = self.firstItemY - 1
        dY = self.firstItemY + self.menuLength
        dX = self.firstItemX + self.maxItemWidth + 1
        return(tX, tY, dX, dY)

    def getSubMenu(self):
        return(self.subMenus)

    def getItemPosition(self, index):
        return((self.firstItemX),
               (self.firstItemY + index)
               )


class TacheMenu(Menu):
    """docstring for TacheMenu"""
    def __init__(self, items, title="Menu"):
        super(Menu, self).__init__()
        self.items = items
        self.menuLength = len(items)
        logging.debug("[menu] je suis un menu et jai une taille de" +
                      str(self.menuLength))
        self.subMenus = []
        i = 0
        for item in self.items:
            logging.debug("[TacheMenu] JE LOAD LES TAGS")
            tmpMenu = TacheTagMenu(item.get_tags())
            tmpMenu.setTopX(len(str(self.items[i])) + len(self.selector) + self.firstItemX)
            tmpMenu.setTopY(self.getFirstItemY() + i)
            self.subMenus.append(tmpMenu)
            i += 1


class TacheTagMenu(Menu):

    def __init__(self, items, topX=0, topY=0, title=""):
        super(Menu, self).__init__()
        self.items = items
        self.menuLength = len(self.items)
        self.padding = 2

    def setTopX(self, topX):
        self.topX = topX
        self.firstItemX = self.topX + self.padding

    def setTopY(self, topY):
        self.topY = topY
        self.firstItemY = topY

    def getItemPosition(self, index):
        totalPadding = self.topX + self.padding
        for item in self.items[:index]:
            totalPadding += len(item.name)+1
        return((totalPadding), (self.topY))


class TagMenu(Menu):
    """docstring for TagMenu"""
    def __init__(self, items, title="Tags"):
        super(Menu, self).__init__()
        self.items = items
        self.menuLength = items.count()
        self.title = title
        self.topX = 100
        self.firstItemX = self.topX + self.padding
        self.firstItemY = self.topY + 1


class MultiMenu(Menu):
    """docstring for MultiMenu"""

    def __init__(self, items, topX=0, topY=0, title="Menu"):
        super(Menu, self).__init__()
        self.items = []
        self.action = {}
        for action in items:
            for actionName, settings in action.items():
                if settings["show"]:
                    self.items.append(actionName)
                    self.action[actionName] = settings["action"]
        self.menuLength = len(self.items)
        self.topX = topX
        self.topY = topY
        self.title = title
        self.firstItemX = self.topX + self.padding + 1
        self.firstItemY = self.topY
        self.selector = ">"


class MagicIndex(object):
    """docstring for MagicIndex"""
    def __init__(self, maxLimit, current=0):
        super(MagicIndex, self).__init__()
        self.previous = 0
        self.maxLimit = maxLimit
        self.current = current

    def goNext(self):
        self.previous = self.current
        self.current += 1
        self.current %= self.maxLimit
        return(self.current)

    def goPrevious(self):
        self.previous = self.current
        self.current -= 1
        if self.current < 0:
            self.current = self.maxLimit - 1
        return(self.current)

    def getCurrent(self):
        return(self.current)

    def setCurrent(self, index):
        self.current = index

    def getPrevious(self):
        return(self.previous)
