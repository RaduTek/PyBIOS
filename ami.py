import math
import term
import textwrap

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


def draw_dialog(w: int, h: int, title: str, buttonBox: bool = True) -> tuple[int, int]:
    tw, th = term.get_size()

    # Calculate center positions
    x = (tw - w) // 2
    y = (th - h) // 2

    # Draw shadow
    term.bgcolor(term.colors.black)
    term.fill(x + 1, y + h, w, 1)
    term.fill(x + w, y + 1, 2, h)

    # Draw dialog box
    term.color(term.colors.bright + term.colors.white)
    term.bgcolor(term.colors.blue)
    term.draw_box(x, y, w, h, [], [h - 2] if buttonBox else [])

    # Draw title text
    term.draw_text_centered(f" {title} ", x + 1, y, w - 2, term.borders["we"])

    # Return position of dialog
    return x, y


def get_max_width(text: str) -> int:
    width = 0
    for l in text.splitlines():
        width = max(len(l), width)
    return width


def get_wrap_height(text: str, w: int) -> int:
    lines = []
    for l in text.splitlines():
        lines += textwrap.wrap(l, w)
    return len(lines)


def draw_message_box_options(
    x: int, y: int, w: int, options: list[str], selected: int = 0
):
    def normal_color():
        term.color(term.colors.bright + term.colors.white)
        term.bgcolor(term.colors.blue)

    def selected_color():
        term.bgcolor(term.colors.black)

    max_width = 0
    total_width = 0
    for opt in options:
        max_width = max(max_width, len(opt))
        total_width += len(opt)

    count_opt = len(options)
    item_spacing = (w - (max_width * count_opt)) // (count_opt + 1)

    normal_color()

    term.set_pos(x, y)
    for i in range(len(options)):
        opt = options[i]
        len_opt = len(opt)
        offset = (max_width - len_opt) // 2

        term.rawprint(" " * (item_spacing + offset))

        if i == selected:
            selected_color()
        term.rawprint(f"[{opt}]")

        if i == selected:
            normal_color()


def message_box(title: str, text: str, options: list[str], selected: int = 0) -> int:
    w, h = term.get_size()

    max_width = get_max_width(text)
    content_width = min(math.floor(w * 0.6), max_width)
    content_height = get_wrap_height(text, content_width)
    dialog_width = content_width + 4
    dialog_height = content_height + 6

    x, y = draw_dialog(dialog_width, dialog_height, title)
    term.draw_textblock_centered(text, x + 2, y + 1, content_width, content_height + 2)

    while True:
        draw_message_box_options(
            x + 1, y + dialog_height - 2, dialog_width - 2, options, selected
        )

        key = term.read_key()

        if key == "LEFT":
            selected = max(0, selected - 1)
        elif key == "RIGHT":
            selected = min(selected + 1, len(options) - 1)
        elif key == "ENTER":
            return selected
        else:
            term.beep()


def get_items_to_draw(items: list[str], selected: int, prev_start: int, prev_end: int):
    start_index = prev_start
    end_index = prev_end

    if selected < prev_start:
        start_index -= prev_start - selected
        end_index -= prev_start - selected
    elif selected >= prev_end:
        start_index += selected - prev_end + 1
        end_index += selected - prev_end + 1

    items_draw = items[start_index:end_index]
    return items_draw, start_index, end_index


def draw_select_box_items(
    x: int,
    y: int,
    w: int,
    h: int,
    items: list[str],
    selected: int,
    prev_start: int,
    prev_end: int,
):
    def normal_color():
        term.color(term.colors.bright + term.colors.white)
        term.bgcolor(term.colors.blue)

    def selected_color():
        term.bgcolor(term.colors.black)

    normal_color()
    term.fill(x, y, w, h)

    items_draw, start_index, end_index = get_items_to_draw(
        items, selected, prev_start, prev_end
    )

    has_items_before = start_index > 0
    has_items_after = end_index < len(items)

    term.draw_text(
        term.arrows["n"] if has_items_before else term.borders["we"], x + w - 1, y - 1
    )
    term.draw_text(
        term.arrows["s"] if has_items_after else term.borders["we"], x + w - 1, y + h
    )

    for i in range(len(items_draw)):
        item = items_draw[i]

        if item == items[selected]:
            selected_color()

        term.draw_text(item, x, y + i)

        if item == items[selected]:
            normal_color()

    return start_index, end_index


def select_box(title: str, items: list[str], selected: int = 0) -> int:
    w, h = term.get_size()

    content_width = len(title) + 4
    for item in items:
        content_width = max(content_width, len(item))
    content_width += 2

    total_height = len(items)
    content_height = min(math.floor(h * 0.6), total_height)

    x, y = draw_dialog(content_width + 2, content_height + 2, title, False)

    prev_start = 0
    prev_end = content_height

    while True:
        prev_start, prev_end = draw_select_box_items(
            x + 1,
            y + 1,
            content_width,
            content_height,
            items,
            selected,
            prev_start,
            prev_end,
        )

        key = term.read_key()

        if key == "UP":
            selected = max(0, selected - 1)
        elif key == "DOWN":
            selected = min(selected + 1, len(items) - 1)
        elif key == "ENTER":
            return selected
        else:
            term.beep()


def select_item(item: object) -> object:
    value = select_box(item["title"], item["values"], item["value"])
    item["value"] = value
    return item


def draw_tabs(tabs: list[str], selected: int):
    def normal_color():
        term.color(term.colors.white)
        term.bgcolor(term.colors.blue)

    def selected_color():
        term.color(term.colors.blue)
        term.bgcolor(term.colors.white)

    normal_color()

    w, h = term.get_size()
    term.fill(1, 2, w, 1)
    term.set_pos(4, 2)

    for i in range(len(tabs)):
        if i == selected:
            selected_color()

        term.rawprint(f" {tabs[i]} ")

        if i == selected:
            normal_color()


def draw_help_area():
    w, h = term.get_size()

    term.color(term.colors.blue)
    term.bgcolor(term.colors.white)

    x = w - help_width + 2
    width = help_width - 2

    term.draw_vsplit(w - help_width, h - 3 - help_keys_count, help_width + 1)
    term.draw_text(help_keys, x, h - 2 - help_keys_count, width, help_keys_count)


def draw_help_text(text: str = ""):
    term.color(term.colors.blue)
    term.bgcolor(term.colors.white)

    w, h = term.get_size()

    x = w - help_width + 2
    width = help_width - 2

    term.fill(x, 4, width, h - 8 - help_keys_count)
    term.draw_text(text, x, 4, width)


def get_sel_index(items: list, offset: int = -1, reverse: bool = False):
    r = range(offset - 1, -1, -1) if reverse else range(offset + 1, len(items))
    for i in r:
        item = items[i]
        if item:
            return i
    return offset


def draw_scrollbar(x: int, y: int, h: int, current: int, total: int):
    if h > total:
        return
    term.color(term.colors.bright + term.colors.black)

    sb_height = math.floor(h / total * (h - 2))
    sb_offset = math.floor(current / total * (h - sb_height - 1))

    term.fill(x, y + 1, 1, h - 1, term.blocks["ls"])

    term.color(term.colors.blue)
    term.draw_text(term.arrows["n"], x, y)
    term.draw_text(term.arrows["s"], x, y + h - 1)
    term.fill(x, y + sb_offset + 1, 1, sb_height, term.blocks["full"])


def draw_items(
    items: list,
    selected: int,
    prev_start: int,
    prev_end: int,
    x: int,
    y: int,
    w: int,
    h: int,
) -> tuple[int, int]:

    def normal_color():
        term.color(term.colors.bright + term.colors.black)

    def selected_color():
        term.color(term.colors.bright + term.colors.white)

    def editable_color():
        term.color(term.colors.blue)

    pw = (w - 2) // 2

    term.bgcolor(term.colors.white)
    term.fill(x, y, w - 1, h)
    draw_scrollbar(x + w - 1, y, h, selected, len(items))

    items_draw, start_index, end_index = get_items_to_draw(
        items, selected, prev_start, prev_end
    )

    normal_color()

    for i in range(len(items_draw)):
        item = items_draw[i]
        if not item:
            continue

        if start_index + i == selected:
            selected_color()
        elif "type" in item:
            editable_color()

        if "type" in item:
            if item["type"] == "subpage":
                term.draw_text(term.arrows["e"], x, y + i)

        term.draw_text(item["title"], x + 2, y + i, pw)

        if "value" in item:
            value = item["value"]

            if "type" in item:
                if item["type"] == "select":
                    value = item["values"][value]

            text = f"[{value}]" if "type" in item else value

            term.draw_text(text, x + 2 + pw, y + i, pw)

        normal_color()

    return start_index, end_index


def exit_func():
    term.reset()
    term.clear()
    term.set_pos(0, 0)
    exit()


def exit_confirm(item):
    r = message_box(
        "Save Changes and Exit", "Save configuration and reset?", ["Yes", "No"]
    )
    if r == 0:
        exit_func()
    return item


def test_dialog(item):
    r = message_box("Title", "Are you sure to perform?", ["Yes", "No"])
    if r == 0:
        item["value"] = "Clear"
    return item


main_items = [
    {
        "title": "Project Version",
        "value": "1.23.4567",
    },
    {
        "title": "Project Build Date",
        "value": "01/01/1970",
    },
    None,
    {
        "title": "System Date",
        "value": "01/01/1970",
        "type": "option",
        "help": "Set the current system date",
        "function": test_dialog,
    },
    {
        "title": "System Time",
        "value": "00:00:00",
        "type": "option",
        "help": "Set the current system time",
    },
    None,
    {
        "title": "Hardware Information",
        "type": "subpage",
        "help": "View details about installed hardware",
    },
]


boot_items = [
    {
        "title": "Boot mode",
        "type": "select",
        "values": [
            "UEFI only",
            "UEFI and CSM",
            "Legacy",
            "Legacy 1",
            "Legacy 2",
            "Legacy 3",
            "Legacy 4",
            "Legacy 5",
            "Legacy 6",
            "Legacy 7",
            "Legacy 8",
            "Legacy 9",
        ],
        "value": 1,
        "help": "Set the UEFI boot mode\nUEFI and CSM = Boot both UEFI and legacy devices\n"
        + "UEFI = Boot only UEFI devices\nLegacy = Boot only legacy devices",
    },
    {
        "title": "Network boot",
        "type": "select",
        "values": ["Disabled", "Enabled"],
        "value": 1,
        "help": "Enable/Disable network boot",
    },
    None,
    {
        "title": "Change boot order",
        "type": "option",
        "help": "Edit the order of boot devices",
        "function": test_dialog,
    },
]


def_pages = [
    {
        "title": "Main",
        "items": main_items,
    },
    {
        "title": "Boot",
        "items": boot_items,
    },
    {
        "title": "Exit",
        "items": [
            {
                "title": "Save Changes and Exit",
                "type": "option",
                "help": "Save changed settings and reset the computer\nF10 can be used for this",
                "function": exit_confirm,
            },
            {
                "title": "Discard Changes and Exit",
                "type": "option",
                "help": "Discard changed settings and reset the computer",
            },
            {
                "title": "Discard Changes",
                "type": "option",
                "help": "Discard changed settings",
            },
            {
                "title": "Restore Defaults",
                "type": "option",
                "help": "Restore all settings to defaults and reset the computer",
            },
        ],
    },
]


def bios_page(pages: list):
    term.clear()
    term.cursor(False)

    page_index = 0

    tabs = []
    for page in pages:
        tabs += [page["title"]]

    keep_index = False

    item_selected = 0
    item_view_start = 0
    item_view_end = 0

    while True:
        w, h = term.get_size()

        # Draw title texts
        term.color(term.colors.bright + term.colors.white)
        term.bgcolor(term.colors.blue)
        term.draw_textblock_centered(title_string, 1, 1, w, 2)
        term.color(term.colors.white)
        term.draw_textblock_centered(version_string, 1, h - 1, w, 2)

        # Draw tabs
        draw_tabs(tabs, page_index)

        # Draw page background
        term.color(term.colors.blue)
        term.bgcolor(term.colors.white)
        term.draw_box(1, 3, w, h - 4, [w - help_width])

        # Draw help sidebar
        draw_help_area()

        page = pages[page_index]
        items = page["items"]
        item_view_start = 0
        item_view_end = h - 6

        if keep_index:
            keep_index = False
        else:
            item_selected = get_sel_index(items)

        while True:
            item = items[item_selected]

            # Draw items
            item_view_start, item_view_end = draw_items(
                items,
                item_selected,
                item_view_start,
                item_view_end,
                2,
                4,
                w - help_width - 2,
                h - 6,
            )

            # Draw help text for currently selected item
            draw_help_text(item["help"] if "help" in item else item["title"])

            # Read key
            term.set_pos(w, h)
            key = term.read_key()

            if key == "UP":
                # Go to previous item
                item_selected = get_sel_index(items, item_selected, True)
            elif key == "DOWN":
                # Go to next item
                item_selected = get_sel_index(items, item_selected)
            elif key == "ENTER":
                # Execute current item's function if available
                keep_index = True
                if "type" in item:
                    if "function" in item:
                        item = item["function"](item)
                    elif item["type"] == "select":
                        item = select_item(item)
                    break
            elif key == "LEFT":
                # Go to previous page
                keep_index = False
                page_index = max(0, page_index - 1)
                break
            elif key == "RIGHT":
                # Go to next page
                keep_index = False
                page_index = min(len(pages) - 1, page_index + 1)
                break
            elif key == "ESC":
                # Go to last page (Exit page)
                page_index = len(pages) - 1
                break
            else:
                term.beep()


def main():
    bios_page(def_pages)


if __name__ == "__main__":
    main()
