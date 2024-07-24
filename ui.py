import bios
import color
import math
import term


def draw_dialog(
    size: term.Size,
    title: str,
    palette: color.Palette,
    buttonBox: bool = True,
) -> tuple[int, int]:
    w, h = size
    tw, th = term.get_size()

    # Calculate center positions
    x = (tw - w) // 2
    y = (th - h) // 2

    # Draw shadow
    term.set_color(palette["shadow"])
    term.fill((x + 1, y + h, w, 1))
    term.fill((x + w, y + 1, 2, h))

    # Draw dialog box
    term.set_color(palette["normal"])
    term.draw_box((x, y, w, h), [], [h - 2] if buttonBox else [])

    # Draw title text
    term.draw_text_centered(f" {title} ", (x + 1, y, w - 2, 1), term.borders["we"])

    # Return position of dialog
    return x, y


def draw_scrollbar(
    rect: term.Rectangle, current: int, total: int, palette: color.Palette
):
    x, y, w, h = rect

    # Don't draw scrollbar if content doesn't overflow
    if h > total:
        return

    # Calculate scrollbar height and thumb position
    sb_height = math.floor(h / total * (h - 2))
    sb_offset = math.floor(current / total * (h - sb_height - 1))

    # Draw scrollbar track
    term.set_color(palette["disabled"])
    term.fill(x, y + 1, 1, h - 1, term.blocks["ls"])

    # Draw arrows and scrollbar thumb
    term.set_color(palette["normal"])
    term.draw_text(term.arrows["n"], x, y)
    term.draw_text(term.arrows["s"], x, y + h - 1)
    term.fill(x, y + sb_offset + 1, 1, sb_height, term.blocks["full"])


def draw_items(
    items: list[bios.Item],
    selected: int,
    previous: bios.Range,
    rect: term.Rectangle,
    palette: color.Palette,
) -> bios.Range:
    x, y, w, h = rect
    pw = (w - 2) // 2

    term.set_color(palette["normal"])
    term.fill((x, y, w - 1, h))
    draw_scrollbar((x + w - 1, y, 1, h), selected, len(items), palette)

    start_index, end_index = bios.get_screen_range(selected, previous)

    items_draw = items[start_index:end_index]
    items_count = len(items_draw)

    term.set_color(palette["disabled"])

    for i in range(items_count):
        item = items_draw[i]
        if not item:
            continue

        if start_index + i == selected:
            term.set_color(palette["selected"])
        elif "type" in item:
            term.set_color(palette["normal"])

        if "type" in item:
            if item["type"] == "subpage":
                term.draw_text(term.arrows["e"], (x, y + i, 1, 1))

        term.draw_text(item["title"], (x + 2, y + i, pw, 1))

        if "value" in item:
            value = item["value"]

            if "type" in item:
                if item["type"] == "select":
                    value = item["values"][value]

            text = f"[{value}]" if "type" in item else value

            term.draw_text(text, (x + 2 + pw, y + i, pw, 1))

        term.set_color(palette["disabled"])

    return start_index, end_index


def draw_message_box_options(
    rect: term.Rectangle,
    options: list[str],
    selected: int,
    palette: color.Palette,
):
    x, y, w, h = rect

    max_width = 0
    total_width = 0
    for opt in options:
        max_width = max(max_width, len(opt))
        total_width += len(opt)

    count_opt = len(options)
    item_spacing = (w - (max_width * count_opt)) // (count_opt + 1)

    term.set_color(palette["normal"])

    term.set_pos((x, y))
    for i in range(len(options)):
        opt = options[i]
        len_opt = len(opt)
        offset = (max_width - len_opt) // 2

        term.rawprint(" " * (item_spacing + offset))

        if i == selected:
            term.set_color(palette["selected"])

        term.rawprint(f"[{opt}]")

        if i == selected:
            term.set_color(palette["normal"])


def message_box(
    title: str,
    text: str,
    options: list[str],
    selected: int,
    palette: color.Palette,
) -> int:
    w, h = term.get_size()

    max_width = term.get_max_width(text)
    content_width = min(math.floor(w * 0.6), max_width)
    content_height = term.get_wrap_height(text, content_width)
    dialog_width = content_width + 4
    dialog_height = content_height + 6

    x, y = draw_dialog((dialog_width, dialog_height), title, palette)
    term.draw_textblock_centered(
        text, (x + 2, y + 1, content_width, content_height + 2)
    )

    while True:
        draw_message_box_options(
            (x + 1, y + dialog_height - 2, dialog_width - 2, 1),
            options,
            selected,
            palette,
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


def draw_select_box_items(
    rect: term.Rectangle,
    items: list[str],
    selected: int,
    previous: bios.Range,
    palette: color.Palette,
):
    x, y, w, h = rect
    term.set_color(palette["normal"])
    term.fill(rect)

    start_index, end_index = bios.get_screen_range(selected, previous)

    items_draw = items[start_index:end_index]
    items_count = len(items_draw)

    has_items_before = start_index > 0
    has_items_after = end_index < len(items)

    term.draw_text(
        term.arrows["n"] if has_items_before else term.borders["we"],
        (x + w - 1, y - 1, 0, 0),
    )
    term.draw_text(
        term.arrows["s"] if has_items_after else term.borders["we"],
        (x + w - 1, y + h, 0, 0),
    )

    for i in range(items_count):
        item = items_draw[i]

        if item == items[selected]:
            term.set_color(palette["selected"])

        term.draw_text(item, (x, y + i, 0, 0))

        if item == items[selected]:
            term.set_color(palette["normal"])

    return start_index, end_index


def select_box(
    title: str,
    items: list[str],
    selected: int,
    palette: color.Palette,
) -> int:
    w, h = term.get_size()

    content_width = len(title) + 4
    for item in items:
        content_width = max(content_width, len(item))
    content_width += 2

    total_height = len(items)
    content_height = min(math.floor(h * 0.6), total_height)

    x, y = draw_dialog(
        (content_width + 2, content_height + 2),
        title,
        palette,
        False,
    )

    current_range: bios.Range = (0, content_height)

    while True:
        current_range = draw_select_box_items(
            (x + 1, y + 1, content_width, content_height),
            items,
            selected,
            current_range,
            palette,
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
