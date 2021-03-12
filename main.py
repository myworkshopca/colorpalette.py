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

def calcparams(sh, sw, margin_y=0, margin_x=1):
    """
    Calculate the parameters need for function paintpalette.
    Parameters
    ----------
    sh number:
      screen height
    sw number:
      screen width
    margin_y:
      set how many rows for margin, top and bottom.
      default is 1
    margin_x:
      set how many columns for margin, left and right.
      default is 2
    """

    # calculate how many rows and columns available for painting.
    # reserve 6 rows for message.
    # all message should be on top of the screen.
    rows = sh - margin_y * 2 -3 
    columns = sw - margin_x * 2

    # decide the starting y, x
    start_y = margin_y + 3
    start_x = margin_x

    # calculate the columns and rows of blocks for each color.
    # There will be at lease 2 rows for each color:
    #  - one row of blocks to show the color,
    #    we could use more than one row if we have enough rows.
    #  - one row to display the color pair id.
    # set the columns of blocks to 4 to get started.
    block_c = 3
    block_r = 1
    # calc the colors per row.
    color_perrow = columns // block_c

    return {
        "start_y": start_y,
        "start_x": start_x,
        "block_c": block_c,
        "block_r": block_r,
        "color_perrow": color_perrow
    }

"""
paint the color palette.
paintpalette(stdscr, start_y, start_x, block_c, block_r, color_perrow, bg_color)
Parameters
----------
stdscr
start_y
  the starting cell's y axis
start_x
  the starting cell's x axis
block_c
  set how many columns to paint for each color
block_r
  set how many rows to paint for each color
color_perrow
  set how many colors to paint for each row.
"""
#def paintpalette(stdscr, center_yx, bg_color):
def paintpalette(stdscr, start_y, start_x, block_c, block_r,
        color_perrow, bg_color):

    # set the block character
    # These not working well for terminal! 🏁 127937 
    # ✸ 10040 ❂ 10050 ✹ 10041
    # █ 9608 ◼ 9724
    # ⚑ 9873 ⚐ 9872
    block = chr(9608)
    #block = chr(9724)

    msg = "Curses Color Palette"
    # print the welcome message y-axis and x-axis
    #stdscr.addstr(sy - 6, center_yx[1] - len(msg) // 2, msg)
    stdscr.addstr(start_y - 3, start_x, msg)
    # how to play.
    msg = "Arrow Key up / down to change background color and ESC to exit!"
    stdscr.addstr(start_y - 2, start_x, msg, curses.COLOR_GREEN)

    # paint the background color here.
    stdscr.addstr(start_y - 1, start_x, 'Backgroud Color: {:0>3}'.format(bg_color), curses.A_REVERSE)
    # any of the color pair will show the background color.
    stdscr.addstr(start_y - 1, start_x + 22, '     ', curses.color_pair(1))
    #stdscr.addstr(start_y - 3, start_x + 22, '     ', curses.color_pair(1))

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
                stdscr.addstr(start_y + yi, start_x + xi, block, the_color)
        
        # paint the color pair id.
        stdscr.addstr(start_y + y * (block_r + 1) + block_r,
                start_x + x * block_c, str(i + 1), the_color)
        # paint a white space to match the block size: block_c
        w_size = block_c - len(str(i))
        stdscr.addstr(' ' * w_size, the_color)

def screen(stdscr):

    # turn off the cursor.
    curses.curs_set(0)

    # get the center of the screen.
    sh, sw = stdscr.getmaxyx()
    #center = [sh // 2, sw // 2]
    center = [sh, sw]

    # calculate the parameters for color palette.
    params = calcparams(sh, sw)

    # paint the center at he top left corner.
    #stdscr.addstr(0, 0, str(center))
    #stdscr.getch()

    # track the background color.
    bg = -1
    initcolors(bg)
    paintpalette(stdscr, params['start_y'], params['start_x'],
            params['block_c'], params['block_r'], params['color_perrow'], bg)

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
            paintpalette(stdscr, params['start_y'], params['start_x'],
                    params['block_c'], params['block_r'],
                    params['color_perrow'], bg)

        elif user_key in [curses.KEY_DOWN, 106]:
            # j (106) for down
            if bg >= 0:
                bg = bg - 1
            else:
                bg = 255
            initcolors(bg)
            paintpalette(stdscr, params['start_y'], params['start_x'],
                    params['block_c'], params['block_r'],
                    params['color_perrow'], bg)

curses.wrapper(screen)
