import curses
 
def main():
    s = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    cpt = 0
    for i in range(-1, 8):
        for y in range(-1, 8):
            curses.init_pair(cpt, y, i)
            s.addstr(str(cpt), curses.color_pair(cpt))
            s.addstr(' ')
            s.refresh()
            cpt += 1
    s.getch()
    curses.endwin()
 
if __name__ == '__main__':
    main()
