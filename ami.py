import math
import term
import color
import bios
import ui


copyright_string = "Copyright (C) 2024 Company Inc."
title_string = f"PyBIOS Setup Utility - {copyright_string}"
version_string = f"Version 1.23.4567. {copyright_string}"

help_width = 27
help_keys = """\u2190\u2192 Select Screen
\u2191\u2193 Select Item
Enter: Select
F1: General Help
F10: Save and Exit
ESC: Exit"""
help_keys_count = len(help_keys.splitlines())

ColorPair = tuple[int, int]

dialog_palette: color.Palette = {
    "normal": (color.blue, color.light + color.white),
    "selected": (color.black, color.light + color.white),
    "shadow": (color.black, color.light + color.black),
}

screen_palette: color.Palette = {
    "normal": (color.white, color.blue),
    "selected": (color.white, color.light + color.white),
    "disabled": (color.white, color.light + color.black),
}

header_palette: color.Palette = {
    "normal": (color.blue, color.light + color.white),
    "selected": (color.white, color.blue),
    "disabled": (color.blue, color.white),
}


def message_box(
    title: str,
    text: str,
    options: list[str],
    selected: int = 0,
    palette: color.Palette = dialog_palette,
) -> int:
    return ui.message_box(title, text, options, selected, palette)


def select_item(item: object):
    value = ui.select_box(
        title=item["title"],
        items=item["values"],
        selected=item["value"],
        palette=dialog_palette,
    )
    item["value"] = value


def draw_tabs(tabs: list[str], selected: int, palette: color.Palette = header_palette):
    term.set_color(palette["disabled"])

    w, h = term.get_size()
    term.fill((1, 2, w, 1))
    term.set_pos((4, 2))

    for i in range(len(tabs)):
        if i == selected:
            term.set_color(palette["selected"])

        term.rawprint(f" {tabs[i]} ")

        if i == selected:
            term.set_color(palette["disabled"])


def draw_help_area():
    w, h = term.get_size()

    term.set_color(screen_palette["normal"])

    x = w - help_width + 2
    width = help_width - 2

    term.draw_vsplit((w - help_width, h - 3 - help_keys_count), help_width + 1)
    term.draw_text(help_keys, (x, h - 2 - help_keys_count, width, help_keys_count))


def draw_help_text(text: str = ""):
    term.set_color(screen_palette["normal"])

    w, h = term.get_size()

    x = w - help_width + 2
    width = help_width - 2

    term.fill((x, 4, width, h - 8 - help_keys_count))
    term.draw_text(text, (x, 4, width, 0))


def bios_screen(pages_gen: bios.PageGenerators):
    term.clear()
    term.cursor(False)

    page_index = 0
    page_total = len(pages_gen)
    item_range: bios.Range = (0, 0)

    tabs = []
    for page_gen in pages_gen:
        page = page_gen()
        tabs += [page["title"]]

    keep_index = False

    while True:
        w, h = term.get_size()

        # Draw title texts
        term.set_color(header_palette["normal"])
        term.draw_textblock_centered(title_string, (1, 1, w, 2))

        term.set_color(header_palette["disabled"])
        term.draw_textblock_centered(version_string, (1, h - 1, w, 2))

        # Draw tabs
        draw_tabs(tabs, page_index)

        # Draw page background
        term.set_color(screen_palette["normal"])
        term.draw_box((1, 3, w, h - 4), [w - help_width])

        # Draw help sidebar
        draw_help_area()

        page = pages_gen[page_index]()
        items = page["items"]

        item_range = (0, h - 7)

        if keep_index:
            keep_index = False
        else:
            item_selected = bios.get_selectable_index(items)

        while True:
            item = items[item_selected]

            # Draw items
            item_range = ui.draw_items(
                items,
                item_selected,
                item_range,
                (2, 4, w - help_width - 2, h - 6),
                screen_palette,
            )

            # Draw help text for currently selected item
            draw_help_text(item["help"] if "help" in item else item["title"])

            # Read key
            term.set_pos((w, h))
            key = term.read_key()

            if key == "UP":
                # Go to previous item
                item_selected = bios.get_selectable_index(items, item_selected, True)
            elif key == "DOWN":
                # Go to next item
                item_selected = bios.get_selectable_index(items, item_selected)
            elif key == "ENTER":
                # Execute current item's function if available
                keep_index = True
                if "type" in item:
                    if "function" in item:
                        item["function"](item)
                    elif item["type"] == "select":
                        select_item(item)
                    break
            elif key == "LEFT":
                # Go to previous page
                keep_index = False
                page_index = max(0, page_index - 1)
                break
            elif key == "RIGHT":
                # Go to next page
                keep_index = False
                page_index = min(page_total - 1, page_index + 1)
                break
            elif key == "ESC":
                # Go to last page (Exit page)
                page_index = page_total - 1
                break
            else:
                term.beep()
