from typing import List, Callable, Any, NotRequired, TypedDict


class Item(TypedDict):
    title: str
    type: NotRequired[str]
    help: NotRequired[str]
    value: NotRequired[Any]
    values: NotRequired[List[Any]]
    function: NotRequired[Callable]


class Page(TypedDict):
    title: str
    items: List[Item]


def get_selectable_index(items: List[Item], offset: int = -1, reverse: bool = False):
    r = range(offset - 1, -1, -1) if reverse else range(offset + 1, len(items))
    for i in r:
        item = items[i]
        if item:
            return i
    return offset


Range = tuple[int, int]


def get_screen_range(selected: int, previous: Range) -> Range:
    prev_start, prev_end = previous

    start_index = prev_start
    end_index = prev_end

    if selected < prev_start:
        start_index -= prev_start - selected
        end_index -= prev_start - selected
    elif selected >= prev_end:
        start_index += selected - prev_end + 1
        end_index += selected - prev_end + 1

    return start_index, end_index


PageGenerator = Callable[[], Page]
PageGenerators = List[PageGenerator]


def new_page_generator(page: Page) -> PageGenerator:
    def generator() -> Page:
        return page

    return generator
