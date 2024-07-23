import os
import math
import textwrap
import termios
import tty
import sys

ESC = "\033["


class colors:
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    white = 37

    back = 10
    bright = 60


def rawprint(*values: object):
    print(*values, sep="", end="", flush=True)


def clear():
    rawprint(ESC, "3J")
    rawprint(ESC, "2J")


def get_size() -> tuple[int, int]:
    col, row = os.get_terminal_size()
    return col, row


def reset():
    rawprint(ESC, "0m")


def color(c: int):
    rawprint(ESC, c, "m")


def bgcolor(c: int):
    rawprint(ESC, colors.back + c, "m")


def set_pos(x: int, y: int):
    rawprint(ESC, y, ";", x, "H")


def fill(x: int, y: int, w: int, h: int, c: str = " "):
    for i in range(y, y + h):
        set_pos(x, i)
        rawprint(c * w)


borderChr = {
    "we": "\u2500",
    "ns": "\u2502",
    "se": "\u250C",
    "sw": "\u2510",
    "ne": "\u2514",
    "nw": "\u2518",
    "nse": "\u251C",
    "nsw": "\u2524",
    "swe": "\u252C",
    "nwe": "\u2534",
    "nswe": "\u253C",
}


class borderProfiles:
    top = borderChr["se"] + borderChr["we"] + borderChr["swe"] + borderChr["sw"]
    middle = borderChr["ns"] + " " + borderChr["ns"] + borderChr["ns"]
    middle_vsplit = (
        borderChr["nse"] + borderChr["we"] + borderChr["nswe"] + borderChr["nsw"]
    )
    bottom = borderChr["ne"] + borderChr["we"] + borderChr["nwe"] + borderChr["nw"]


def gen_box_line(w: int, splits: list[int], chars: str) -> str:
    line = chars[0]
    for split in splits:
        line += chars[1] * (split - len(line) - 1) + chars[2]
    line += chars[1] * (w - len(line) - 1) + chars[3]
    return line


def draw_box(
    x: int,
    y: int,
    w: int,
    h: int,
    hsplit: list[int] = [],
    vsplit: list[int] = [],
):
    line_t = gen_box_line(w, hsplit, borderProfiles.top)
    line = gen_box_line(w, hsplit, borderProfiles.middle)
    line_s = gen_box_line(w, hsplit, borderProfiles.middle_vsplit)
    line_b = gen_box_line(w, hsplit, borderProfiles.bottom)

    set_pos(x, y)
    rawprint(line_t)

    for i in range(y + 1, y + h - 1):
        set_pos(x, i)
        if (i - y + 1) in vsplit:
            rawprint(line_s)
        else:
            rawprint(line)

    set_pos(x, y + h - 1)
    rawprint(line_b)


def cursor(enabled: bool = True):
    rawprint(ESC, "?25", "h" if enabled else "l")


def draw_vsplit(x: int, y: int, w: int):
    line = gen_box_line(w, [], borderProfiles.middle_vsplit)
    set_pos(x, y)
    rawprint(line)


def draw_text(text: str, x: int, y: int, w: int = 0, h: int = 0):
    if w == 0 and h == 0:
        set_pos(x, y)
        rawprint(text)
    else:
        lines = []
        for l in text.splitlines():
            lines += textwrap.wrap(l, w)

        for i in range(len(lines)):
            set_pos(x, y + i)
            rawprint(lines[i])


def draw_text_centered(text: str, x: int, y: int, w: int, h: int, spaceChr: str = " "):
    lines = []
    for l in text.splitlines():
        lines += textwrap.wrap(l, w)

    if len(lines) < h:
        extra = h - len(lines)
        lines = ([""] * math.floor(extra / 2)) + lines + ([""] * math.ceil(extra / 2))

    for i in range(h):
        set_pos(x, y + i)
        extra = w - len(lines[i])
        rawprint(
            spaceChr * math.floor(extra / 2), lines[i], spaceChr * math.ceil(extra / 2)
        )


def beep():
    rawprint("\x07")


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def read_key():
    c1 = getch()

    if c1 == "\x1b":
        c2 = getch()
        if c2 == "[":
            c3 = getch()
            if c3 == "A":
                return "UP"
            elif c3 == "B":
                return "DOWN"
            elif c3 == "C":
                return "RIGHT"
            elif c3 == "D":
                return "LEFT"
            elif c3 in "OPQRS":  # F1-F4
                return f'F{ord(c3) - ord("O") + 1}'
            else:
                c4 = getch()
                if c3 == "1":
                    if c4 == "5":
                        return "F5"
                    elif c4 == "7":
                        return "F6"
                    elif c4 == "8":
                        return "F7"
                    elif c4 == "9":
                        return "F8"
                elif c3 == "2":
                    if c4 == "0":
                        return "F9"
                    elif c4 == "1":
                        return "F10"
                    elif c4 == "3":
                        return "F11"
                    elif c4 == "4":
                        return "F12"
        else:
            return "ESC"
    elif c1 in ["\n", "\r"]:
        return "ENTER"

    return c1
