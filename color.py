from typing import TypedDict

Color = int


black: Color = 30
red: Color = 31
green: Color = 32
yellow: Color = 33
blue: Color = 34
magenta: Color = 35
cyan: Color = 36
white: Color = 37

back: Color = 10
light: Color = 60


Pair = tuple[Color, Color]


class Palette(TypedDict):
    normal: Pair
    selected: Pair
    disabled: Pair
    shadow: Pair
