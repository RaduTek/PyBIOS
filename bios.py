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


PageGenerator = Callable[[], Page]
PageGenerators = List[PageGenerator]


def new_page_generator(page: Page) -> PageGenerator:
    def generator() -> Page:
        return page

    return generator
