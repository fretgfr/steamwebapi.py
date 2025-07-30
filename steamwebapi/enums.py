"""
Copyright 2025-present fretgfr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from enum import Enum

__all__ = ("Game", "Language", "SortOrder", "Wear", "ItemGroup", "ItemType", "InventoryState")


class Game(Enum):
    """Games supported by the API."""

    CS2 = "cs2"
    RUST = "rust"
    DOTA = "dota"


class Language(Enum):
    """Languages supported by the API."""

    Danish = "danish"
    English = "english"
    French = "french"
    German = "german"
    Polish = "polish"
    Portuguese = "portuguese"
    Russian = "russian"
    Swedish = "swedish"
    Turkish = "turkish"


class Wear(Enum):
    """Wears that an item can have."""

    factory_new = "fn"
    minimal_wear = "mw"
    field_tested = "ft"
    well_worn = "ww"
    battle_scarred = "bs"


class SortOrder(Enum):
    """Sorting order for item requests."""

    price_asc = "priceAz"
    price_desc = "priceZa"
    price_real_asc = "priceRealAz"
    price_real_desc = "priceRealZa"
    win_loss_asc = "winLossAz"
    win_loss_desc = "winLossZa"
    sold_asc = "soldAz"
    sold_desc = "soldZa"
    item_name = "name"
    points_asc = "pointsAz"
    points_desc = "pointsZa"
    winner = "winner"
    loser = "loser"


class ItemGroup(Enum):
    pass


class ItemType(Enum):
    pass


class ScreenshotColorScheme(Enum):
    """Valid color schemes for item screenshot generation."""

    black = "black"
    blue = "blue"
    green = "green"
    orange = "orange"
    purple = "purple"
    red = "red"
    white = "white"
    yellow = "yellow"
    gray = "gray"


class ScreenshotLogoOffset(Enum):
    """Valid logo offset start points for screenshot generation."""

    top_left = "top left"
    top_right = "top right"
    bottom_left = "bottom left"
    bottom_right = "bottom right"


class ScreenshotFormat(Enum):
    """Valid options for the format parameter when generating screenshots."""

    screen = "screen"  # TODO: Probably describe these better? Better names maybe?
    download = "download"
    base64 = "base64"


class InventoryState(Enum):
    """Valid inventory states when making inventory requests."""

    active = "active"
    fallback = "fallback"
    takedb = "takedb"  # TODO: what do these mean...


class ItemHistoryOrigin(Enum):
    """Valid values for the origin parameter of item history requests."""

    steamwebapi = "steamwebapi"
    markets = "markets"


class ItemHistoryType(Enum):
    """Valid values for the type parameter of item history requests."""

    sell = "sell"
    offer = "offer"
    median = "median"


class ItemHistorySource(Enum):
    """Valid values for the source parameter of item history requests."""

    steam = "steam"
    skinport = "skinport"
