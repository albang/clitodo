#!/usr/bin/env python
import logging

class Menu(object):
    """docstring for Menu

     This class is the mother class of menu

    """
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
        """
            this function return the number of his items
        """ 
        return(self.menuLength)

    def getItems(self):
        """
            this function return all items 
        """ 
        return(self.items)

    def moveUp(self):
        """
            this function select the item before in the list 
        """ 
        logging.debug("[menu]Move up")
        if self.menuLength > 0:
            self.previousIndex = self.selectedIndex
            self.selectedIndex -= 1
            if self.selectedIndex < 0:
                self.selectedIndex = self.menuLength - 1
        else:
            logging.info("[menu]Move up is impossible\
                          Menu is empty")
        return(self.menuLength > 0)

    def moveDown(self):
        """
            this function select the item after in the list 
        """ 
        logging.debug("[menu]Move down")
        if self.menuLength > 0:
            self.previousIndex = self.selectedIndex
            self.selectedIndex += 1
            self.selectedIndex %= self.menuLength
        else:
            logging.info("[menu]Move down is impossible\
                          Menu is empty")
        return(self.menuLength > 0)

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def isSelected(self, index):
        """
            this function return true if the index is sectected
            :param arg1: index
            :type arg1: int
        """
        return(index == self.selectedIndex)

    def noSelection(self):
        """
            this function deselect the item
        """
        logging.debug("[" + self.title + "] noselection index" +
                      str(self.selectedIndex))
        self.previousIndex = self.selectedIndex
        self.selectedIndex = -1

    def selection(self, index=0):
        """
            this function select the item and deal with the previous item
            :param arg1: index
            :type arg1: int
        """
        if index >= self.menuLength:
            logging.error("[menu][selection] index (" +
                          str(index) + ")is out of range(" +
                          str(menuLength) +
                          ")")
        else:
            self.previousIndex = self.selectedIndex
            self.selectedIndex = index
            logging.debug("[" + self.title + "] selection index" +
                          str(self.selectedIndex))

    def getSelected(self):
        """
            this function return the selected item/object
        """
        logging.info("[menu][GetSelected] " +
                     self.title + " " + str(self.selectedIndex))
        return(self.items[self.selectedIndex])

    def getPrevious(self):
        """
            this function return the selected previous item/object (not good)
        """
        if self.menuLength >= 1 and self.previousIndex != -1:
            logging.info("[menu][GetSelected] " +
                         self.title + " " + str(self.selectedIndex))
            return(self.items[self.previousIndex])

    def getSelectedIndex(self):
        """
            this function return the selected index
        """
        return(self.selectedIndex)

    def getPreviousIndex(self):
        """
            this function return the selected previous selected index
        """
        return(self.previousIndex)

    def getSelectedPosition(self):
        """ is it compliant with getFirstItemY & getFirstItemY ?
            it can be better
        """
        return(
               (self.topX + self.padding + len(self.selector)),
               (self.topY + 1 + self.selectedIndex)
               )

    def getItemLength(self):
        """
            This function return the lenght of str representation of the selected index
        """
        return(len(str(self.items[self.selectedIndex])))

    def performAction(self):
        """
            Tricky function witch permit to do things
            More to say ... later
        """
        return(self.action[self.getSelected()]())

    def setTopX(self, topX):
        """
            This function set the X coordinate of the left corner of the menu
            And update the First item x (Warning of the selector length)
        """
        self.topX = topX
        self.firstItemX = self.topX + self.padding

    def getTopX(self):
        """
            This function get the X coordinate of the left corner of the menu 
        """
        return(self.topX)

    def setTopY(self, topY):
        """
            This function set the Y coordinate of the left corner of the menu
            And update the First item Y
        """
        self.topY = topY
        self.firstItemY = topY + 1

    def getTopY(self):
        """
            This function get the X coordinate of the left corner of the menu
        """
        return(self.topY)

    def getFirstItemX(self):
        """
            This function set the x coordinate of the first item of the menu
        """
        return(self.firstItemX)

    def getFirstItemY(self):
        """
            This function set the y coordinate of the first item of the menu
        """
        return(self.firstItemY)

    def getSelector(self):
        """
            this function return selector of the menu
        """
        return(self.selector)

    def getTitle(self):
        """
            this function return tittle of the menu
        """
        return(self.title)

    @property
    def maxItemWidth(self):
        """
            this property return the biggest length of all items (not good) 
        """
        maxWidth = 0
        for item in self.items:
            if len(str(item)) > maxWidth:
                maxWidth = (len(str(item)))
        return(maxWidth)

    def entoureMe(self):
        """
            this function return 2 point first one is the top left corner(x,y)
            and the second is the down right corner 
        """
        tX = self.firstItemX - len(self.selector)
        tY = self.firstItemY - 1
        dY = self.firstItemY + self.menuLength
        dX = self.firstItemX + self.maxItemWidth + 1
        return(tX, tY, dX, dY)

    def getSubMenu(self):
        """
           is it a kind of  recursive fonction ? no, is not! 
        """
        return(self.subMenus)

    def getItemPosition(self, index):
        """
           This function return a tuple of the position (x,y) of a object
            :param arg1: index
            :type arg1: int
        """
        return((self.firstItemX),
               (self.firstItemY + index)
               )

    def setFirstItemX(self, newX):
        """
           This function can override the setFirstItemX
           :param arg1: newX
           :type arg1: int
        """
        self.firstItemX = newX

    def setFirstItemY(self, newY):
        """
           This function can override the setFirstItemY
           :param arg1: newY
           :type arg1: int
        """
        self.firstItemY = newY

    def getLastItemY(self):
        """
           This function can return the next line after the last item 
        """
        return(self.firstItemY + self.menuLength)

    def reload(self, items):
        """
           This function reload items menu
        """
        self.items = items
        self.menuLength = items.count()



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
            tmpMenu.noSelection()
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

class MetaMenu(Menu):
    """docstring for MetaMenu"""

    def __init__(self, items, topX=0, topY=0, title="Menu"):
        super(Menu, self).__init__()
        #blablabla



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
