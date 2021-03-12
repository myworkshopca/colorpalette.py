import curses
import random

# initialize colors.
def initcolors(bg_color=-1):

    # initialize the color pair
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
    #for i in range(0, 20):
        # pair number, foreground color, background color
        #curses.init_pair(i + 1, i, -1)
        curses.init_pair(i + 1, i, bg_color)
        #curses.init_pair(i + 1, i, 8)
        the_color = curses.color_pair(i + 1)

def paintpalette(stdscr, center_yx, bg_color):

    # set the block character
    # These not working well for terminal! 🏁 127937 
    # ✸ 10040 ❂ 10050 ✹ 10041
    # █ 9608 ◼ 9724
    # ⚑ 9873 ⚐ 9872
    #block = chr(9608)
    block = chr(9724)
    # set the block column and rows
    block_c = 4
    block_r = 1
    # set how many colors for each row.
    color_perrow = 16

    # calculate the starting cell's y, x axis
    #sy = center_yx[0] - (curses.COLORS // color_perrow)
    sy = 7 
    sx = center_yx[1] - (color_perrow * block_c) // 2

    msg = "Curses Color Palette"
    # print the welcome message y-axis and x-axis
    stdscr.addstr(sy - 6, center_yx[1] - len(msg) // 2, msg)
    # how to play.
    msg = "Arrow Key up / down to change background color and ESC to exit!"
    stdscr.addstr(sy - 5, center_yx[1] - len(msg) // 2, msg, curses.COLOR_GREEN)

    # paint the background color here.
    stdscr.addstr(sy - 3, sx, 'Backgroud Color: {:0>3}'.format(bg_color), curses.A_REVERSE)
    stdscr.addstr(sy - 3, sx + 22, '     ', curses.color_pair(10))
    stdscr.addstr(sy - 2, sx + 22, '     ', curses.color_pair(10))

    for i in range(0, curses.COLORS):
    #for i in range(0, 20):
        #curses.init_pair(i + 1, i, 8)
        the_color = curses.color_pair(i + 1)

        # calculate the row index
        y = i // color_perrow
        # calculate the column index
        x = i % color_perrow

        #stdscr.addstr("<{0}>".format(i + 1), curses.color_pair(i + 1))
        # the ragne will inclue the first one not the last number
        # paint the color blocks
        for xi in range(x * block_c, x * block_c + block_c):
            for yi in range(y * (block_r + 1), y * (block_r + 1) + block_r):
                stdscr.addstr(sy + yi, sx + xi, block, the_color)
        
        # paint the color pair id.
        stdscr.addstr(sy + y * (block_r + 1) + block_r, sx + x * block_c, str(i + 1), the_color)
        # paint a white space to match the block size: block_c
        w_size = block_c - len(str(i))
        stdscr.addstr(' ' * w_size, the_color)

def screen(stdscr):

    # turn off the cursor.
    curses.curs_set(0)

    # get the center of the screen.
    sh, sw = stdscr.getmaxyx()
    center = [sh // 2, sw // 2]


    # track the background color.
    bg = -1
    initcolors(bg)
    paintpalette(stdscr, center, bg)

    while True:
        user_key = stdscr.getch()

        # exit when user press ESC q or Q
        if user_key in [27, 113, 81]:
            break;

        # decide the new head based on the direction
        if user_key in [curses.KEY_UP, 107]:
            # k (107) for up
            if bg < curses.COLORS - 1:
                bg = bg + 1
            else:
                bg = -1
            initcolors(bg)
            paintpalette(stdscr, center, bg)

        elif user_key in [curses.KEY_DOWN, 106]:
            # j (106) for down
            if bg >= 0:
                bg = bg - 1
            else:
                bg = 255
            initcolors(bg)
            paintpalette(stdscr, center, bg)

curses.wrapper(screen)
