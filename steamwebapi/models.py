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

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional

from .utils import parse_timestamp

__all__ = (
    "AccountInformation",
    "FloatData",
    "InventoryItem",
    "InventoryHistoryEntry",
    "ItemAction",
    "ItemAutocompleteResult",
    "ItemDescription",
    "ItemTag",
    "KeychainData",
    "MarketPrice",
    "OwnerDescription",
    "ParsedInspectLink",
    "SteamSale",
    "StickerData",
)


@dataclass
class AccountInformation:
    info: Dict[str, Any]
    minute: int
    hour: int
    today: int
    yesterday: int
    week: int
    month: int
    package: str
    subscription_start: str
    subscription_end: str
    steamwebapi_status: Dict[str, Any]  # TODO
    last_100: List[Dict[str, Any]]  # TODO

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> AccountInformation:
        return cls(
            data["info"],
            data["minute"],
            data["hour"],
            data["today"],
            data["yesterday"],
            data["week"],
            data["month"],
            data["package"],
            data["subscriptionstart"],
            data["subscriptionuntil"],
            data["steamwebapistatus"],
            data["last100"],
        )


class Currency:

    __slots__ = ("symbol", "rate", "precision")

    def __init__(self, symbol: str, rate: float, precision: int):
        self.symbol = symbol
        self.rate = rate
        self.precision = precision


@dataclass
class ExchangeRates:

    __slots__ = ("rates", "base")

    rates: List[Currency]
    base: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ExchangeRates:
        base = data["base"]

        currencies = []
        for symbol in data["rates"].keys():
            rate = data["rates"][symbol]
            precision = data["precision"][symbol]

            currencies.append(Currency(symbol, rate, precision))

        return cls(currencies, base)

    @property
    def symbols(self) -> List[str]:
        """Returns a list of available ISO 4217 symbols that are available."""
        return [c.symbol for c in self.rates]

    def to_mapping(self) -> Mapping[str, Currency]:
        """Returns a mapping of ISO 4217 codes to their :class:`~steamwebapi.models.Currency` object."""
        return {c.symbol: c for c in self.rates}


@dataclass
class FloatData:
    __slots__ = (
        "float",
        "phase",
        "type",
        "origin",
        "paint_seed",
        "paint_index",
        "rank",
        "def_index",
        "rarity",
        "quality",
        "total_count",
        "wear",
        "min",
        "max",
        "has_sticker",
        "has_keychain",
        "sticker_amount",
        "keychain_amount",
        "stickers",
        "keychains",
    )

    float: float
    phase: Optional[str]
    type: str
    origin: float  # TODO: Confirm
    paint_seed: int
    paint_index: int
    rank: Optional[int]
    def_index: int  # TODO: Confirm
    rarity: int  # TODO: Confirm
    quality: int  # TODO: Confirm
    total_count: Optional[int]
    wear: str
    min: float
    max: float
    has_sticker: bool
    has_keychain: bool
    sticker_amount: int
    keychain_amount: int
    stickers: List[StickerData]
    keychains: List[KeychainData]

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> FloatData:
        return cls(
            data["float"],
            data.get("phase"),
            data["type"],
            data["origin"],
            data["paintseed"],
            data["paintindex"],
            data.get("rank"),
            data["defindex"],
            data["rarity"],
            data["quality"],
            data.get("totalcount"),
            data["wear"],
            data["min"],
            data["max"],
            data["hassticker"],
            data["haskeychain"],
            data["stickeramount"],
            data["keychainamount"],
            [StickerData._from_data(sub) for sub in data["stickers"]],
            [KeychainData._from_data(sub) for sub in data["keychains"]],
        )


@dataclass
class InventoryHistoryEntry:
    __slots__ = ("item_name", "transaction_date", "action", "game")
    item_name: str
    transaction_date: datetime.datetime
    action: str  # TODO: maybe an enum?
    game: str  # TODO: Maybe an enum?

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> InventoryHistoryEntry:
        return cls(
            data["item_name"],
            parse_timestamp(data["transaction_date"]),
            data["action"],
            data["game"],
        )


@dataclass
class InventoryItem:
    __slots__ = (
        "id",
        "market_hash_name",
        "normalized_name",
        "market_name",
        "slug",
        "count",
        "asset_id",
        "class_id",
        "instance_id",
        "group_id",
        "info_price",
        "price_latest",
        "price_latest_sell",
        "price_latest_sell_24h",
        "price_latest_sell_7d",
        "price_latest_sell_30d",
        "price_latest_sell_90d",
        "latest_item_sell_at",
        "latest_10_steam_sales",
        "price_median",
        "price_median_24h",
        "price_median_7d",
        "price_median_30d",
        "price_median_90d",
        "price_avg",
        "price_avg_24h",
        "price_avg_7d",
        "price_avg_30d",
        "price_avg_90d",
        "price_safe",
        "price_min",
        "price_max",
        "price_mix",
        "buy_order_price",
        "buy_order_median",
        "buy_order_avg",
        "buy_order_volume",
        "offer_volume",
        "sold_today",
        "sold_24h",
        "sold_7d",
        "sold_30d",
        "sol_90d",
        "sold_total",
        "hours_to_sold",
        "points",
        "price_udpated_at",
        "nametag",
        "border_color",
        "color",
        "quality",
        "rarity",
        "image",
        "item_image",
        "marketable",
        "tradable",
        "unstable",
        "unstable_reason",
        "tags",
        "descriptions",
        "actions",
        "created_at",
        "first_seen_time",
        "first_seen_at",
        "steam_url",
        "inspect_link",
        "inspect_link_parsed",
        "market_tradable_restriction",
        "tag1",
        "tag2",
        "tag3",
        "tag4",
        "tag5",
        "tag6",
        "tag7",
        "info_price_real",
        "price_real",
        "price_real_24h",
        "price_real_7d",
        "price_real_30d",
        "price_real_90d",
        "price_real_median",
        "win_loss",
        "prices",
        "float",
        "owner_description",
        "trade_block_until",
    )

    id: str
    market_hash_name: str
    normalized_name: Optional[str]
    market_name: str
    slug: str
    count: int
    asset_id: str  # Missing for Item
    class_id: str
    instance_id: str
    group_id: str
    info_price: str
    price_latest: float
    price_latest_sell: float
    price_latest_sell_24h: float
    price_latest_sell_7d: float
    price_latest_sell_30d: float
    price_latest_sell_90d: float
    latest_item_sell_at: Optional[
        datetime.datetime
    ]  # Not the same for Item, instead its a dict with a 'date', 'timezone_type', and 'timezone' key
    latest_10_steam_sales: Optional[List[SteamSale]]  # Close, but not the same information from the looks of it for Item
    price_median: float
    price_median_24h: float
    price_median_7d: float
    price_median_30d: float
    price_median_90d: float
    price_avg: float
    price_avg_24h: float
    price_avg_7d: float
    price_avg_30d: float
    price_avg_90d: float
    price_safe: float
    price_min: float
    price_max: float
    price_mix: float
    buy_order_price: float
    buy_order_median: float
    buy_order_avg: float
    buy_order_volume: float
    offer_volume: float
    sold_today: int
    sold_24h: int
    sold_7d: int
    sold_30d: int
    sol_90d: int
    sold_total: int
    hours_to_sold: float  # TODO: Confirm
    points: float  # TODO: Confirm
    price_udpated_at: (
        datetime.datetime
    )  # Close for Item, but instead is a dict with 'date', 'timezone_type' and 'timezone' keys
    nametag: Optional[str]
    border_color: str
    color: str
    quality: str
    rarity: Optional[str]
    image: str  # TODO: URL
    item_image: Optional[str]  # Missing for Item
    marketable: bool
    tradable: bool
    unstable: Optional[bool]
    unstable_reason: Optional[str]
    tags: Optional[List[ItemTag]]
    descriptions: Optional[List[ItemDescription]]
    actions: Optional[List[ItemAction]]  # Missing for Item
    created_at: Optional[
        datetime.datetime
    ]  # close for Item, instead its a dict with 'date', 'timezone_type' and 'timezone' as keys
    first_seen_time: Optional[float]  # TODO Confirm
    first_seen_at: Optional[
        datetime.datetime
    ]  # Close for Item, instead its a dict with 'date', 'timezone_type' and 'timezone' as keys
    steam_url: str
    inspect_link: Optional[str]  # Missing for Item
    inspect_link_parsed: Optional[ParsedInspectLink]  # Missing for item
    market_tradable_restriction: Optional[str]
    tag1: Optional[str]
    tag2: Optional[str]
    tag3: Optional[str]
    tag4: Optional[str]
    tag5: Optional[str]
    tag6: Optional[str]
    tag7: Optional[str]
    info_price_real: Optional[str]
    price_real: Optional[float]
    price_real_24h: Optional[float]
    price_real_7d: Optional[float]
    price_real_30d: Optional[float]
    price_real_90d: Optional[float]
    price_real_median: Optional[float]
    win_loss: Optional[float]  # TODO: Confirm
    # Item has a 'winlossprice', 'groupname', 'wear', 'isstar', 'isstattrak', 'issouvenir', 'itemgroup', 'itemname' here.
    prices: Optional[List[MarketPrice]]
    float: Optional[FloatData]  # missing for Item
    owner_description: Optional[List[OwnerDescription]]  # Missing for Item
    trade_block_until: Optional[str]  # Missing for Item

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> InventoryItem:
        return cls(
            data["id"],
            data["markethashname"],
            data.get("normalizedname"),
            data["marketname"],
            data["slug"],
            data["count"],
            data["assetid"],
            data["classid"],
            data["instanceid"],
            data["groupid"],
            data["infoprice"],
            data["pricelatest"],
            data["pricelatestsell"],
            data["pricelatestsell24h"],
            data["pricelatestsell7d"],
            data["pricelatestsell30d"],
            data["pricelatestsell90d"],
            parse_timestamp(data["lateststeamsellat"]) if "lateststeamsellat" in data else None,
            [SteamSale._from_data(sub) for sub in data["latest10steamsales"]] if "latest10steamsales" in data else None,
            data["pricemedian"],
            data["pricemedian24h"],
            data["pricemedian7d"],
            data["pricemedian30d"],
            data["pricemedian90d"],
            data["priceavg"],
            data["priceavg24h"],
            data["priceavg7d"],
            data["priceavg30d"],
            data["priceavg90d"],
            data["pricesafe"],
            data["pricemin"],
            data["pricemax"],
            data["pricemix"],
            data["buyorderprice"],
            data["buyordermedian"],
            data["buyorderavg"],
            data["buyordervolume"],
            data["offervolume"],
            data["soldtoday"],
            data["sold24h"],
            data["sold7d"],
            data["sold30d"],
            data["sold90d"],
            data["soldtotal"],
            data["hourstosold"],
            data["points"],
            parse_timestamp(data["priceupdatedat"]),
            data.get("nametag"),
            data["bordercolor"],
            data["color"],
            data["quality"],
            data.get("rarity"),
            data["image"],
            data.get("itemimage"),
            data["marketable"],
            data["tradable"],
            data.get("unstable"),
            data.get("unstablereason"),
            [ItemTag._from_data(sub) for sub in data["tags"]] if "tags" in data else None,
            [ItemDescription._from_data(sub) for sub in data["descriptions"]] if "descriptions" in data else None,
            [ItemAction._from_data(sub) for sub in data["actions"]] if "actions" in data else None,
            parse_timestamp(data["createdat"]) if "createdat" in data else None,
            data.get("firstseentime"),
            parse_timestamp(data["firstseenat"]) if "firstseenat" in data else None,
            data["steamurl"],
            data.get("inspectlink"),
            ParsedInspectLink._from_data(data["inspectlinkparsed"]) if "inspectlinkparsed" in data else None,
            data.get("markettradablerestriction"),
            data.get("tag1"),
            data.get("tag2"),
            data.get("tag3"),
            data.get("tag4"),
            data.get("tag5"),
            data.get("tag6"),
            data.get("tag7"),
            data.get("infopricereal"),
            data.get("pricereal"),
            data.get("pricereal24h"),
            data.get("pricereal7d"),
            data.get("pricereal30d"),
            data.get("pricereal90d"),
            data.get("pricerealmedian"),
            data.get("winloss"),
            [MarketPrice._from_data(sub) for sub in data["prices"]] if "prices" in data else None,
            FloatData._from_data(data["float"]) if "float" in data else None,
            [OwnerDescription._from_data(sub) for sub in data["ownerdescription"]] if "ownerdescription" in data else None,
            data.get("tradeblockuntil"),
        )

    @property
    def tradeable(self) -> bool:
        """Alias for :attr:`tradable`."""
        return self.tradable

    @property
    def market_tradeable_restriction(self) -> Optional[str]:
        """Alias for :attr:`market_tradable_restriction`."""
        return self.market_tradable_restriction


@dataclass
class Item:  # TODO

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> Item:
        return cls()


@dataclass
class ItemAction:
    __slots__ = ("link", "name")

    link: str
    name: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ItemAction:
        return cls(data["link"], data["name"])


@dataclass
class ItemAutocompleteResult:
    __slots__ = ("market_hash_name", "image")

    market_hash_name: str
    image: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ItemAutocompleteResult:
        return cls(data["markethashname"], data["image"])


@dataclass
class ItemDescription:
    __slots__ = ("types", "value", "color")

    type: str
    value: str
    color: Optional[str]

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ItemDescription:
        return cls(data["type"], data["value"], data.get("color"))


@dataclass
class ItemHistoryEntry:
    __slots__ = ("id", "created_at", "price", "sold")
    id: int
    created_at: datetime.datetime
    price: float
    sold: Optional[bool]

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ItemHistoryEntry:
        return cls(
            data["id"],
            parse_timestamp(data["createdat"]),
            data["price"],
            data.get("sold"),
        )


@dataclass
class ItemTag:
    __slots__ = (
        "category",
        "internal_name",
        "localized_category_name",
        "localized_tag_name",
        "color",
    )

    category: str
    internal_name: str
    localized_category_name: str
    localized_tag_name: str
    color: Optional[str]

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ItemTag:
        return cls(
            data["category"],
            data["internal_name"],
            data["localized_category_name"],
            data["localized_tag_name"],
            data.get("color"),
        )


@dataclass
class KeychainData:
    __slots__ = (
        "slot",
        "keychain_id",
        "name",
        "image",
    )

    slot: int
    keychain_id: int  # TODO: Confirm
    name: str
    image: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> KeychainData:
        return cls(
            data["slot"],
            data["keychain_id"],
            data["name"],
            data["image"],
        )


@dataclass
class MarketPrice:
    __slots__ = (
        "market",
        "price",
        "url",
        "currency",
        "updated_at",
    )

    market: str
    price: float
    url: str
    currency: str
    updated_at: datetime.datetime

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> MarketPrice:
        return cls(
            data["market"],
            data["price"],
            data["url"],
            data["currency"],
            parse_timestamp(data["updated_at"]),
        )


@dataclass
class OwnerDescription:
    __slots__ = ("type", "value", "color")

    type: str
    value: str
    color: Optional[str]

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> OwnerDescription:
        return cls(
            data["type"],
            data["value"],
            data.get("color"),
        )


@dataclass
class ParsedInspectLink:
    __slots__ = ("s", "a", "d", "m")

    s: str
    a: str
    d: str
    m: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> ParsedInspectLink:
        return cls(
            data["s"],
            data["a"],
            data["d"],
            data["m"],
        )


@dataclass
class Profile:
    __slots__ = (
        "steam_id",
        "persona_name",
        "account_name",
        "profile_url",
        "profile_steam_url",
        "avatar_hash",
        "avatar",
        "avatar_medium",
        "avatar_full",
        "real_name",
        "community_visibility_message",
        "community_visibility_state",
        "profile_state",
        "online_state",
        "ingame_info",
        "time_created",
        "time_created_at",
        "location",
        "location_country_code",
        "summary",
        "vac",
        "is_limited",
        "most_played_games_total_playtime",
        "most_played_games_2_weeks_playtime",
        "most_played_games_app_ids",
        "most_played_games",
        "most_played_games_times",
        "friends_state",
        "friends_count",
        "games_count",
        "groups_count",
        "badges_count",
        "trade_ban",
        "game_ban",
        "last_ban_days",
        "level",
    )

    steam_id: str
    persona_name: str
    account_name: str
    profile_url: Optional[str]
    profile_steam_url: str
    avatar_hash: str
    avatar: str
    avatar_medium: str
    avatar_full: str
    real_name: Optional[str]
    community_visibility_message: str
    community_visibility_state: int
    profile_state: int
    online_state: str
    ingame_info: List[Any]  # TODO: Confirm type
    time_created: int  # Unix timestamp
    time_created_at: str  # ISO Format datetime, +00:00 so no parse_iso_timestamp :angery:
    location: Optional[str]  # TODO: Confirm type
    location_country_code: Optional[str]  # TODO: confirm type
    summary: str
    vac: int
    is_limited: int
    most_played_games_total_playtime: Optional[Any]  # TODO: Confirm type
    most_played_games_2_weeks_playtime: Optional[Any]  # TODO: Confirm type
    most_played_games_app_ids: List[Any]  # TODO: Confirm type
    most_played_games: List[Any]  # TODO: Confirm type
    most_played_games_times: List[Any]  # TODO: Confirm type
    friends_state: int
    friends_count: int
    games_count: int
    groups_count: Optional[int]
    badges_count: Optional[int]
    trade_ban: int
    game_ban: int
    last_ban_days: Optional[int]
    level: int

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> Profile:  # TODO
        return cls(
            data["steamid"],
            data["personaname"],
            data["accountname"],
            data["profileurl"],
            data["profilesteamurl"],
            data["avatarhash"],
            data["avatar"],
            data["avatarmedium"],
            data["avatarfull"],
            data["realname"],
            data["communityvisibilitymessage"],
            data["communityvisibilitystate"],
            data["profilestate"],
            data["onlinestate"],
            data["ingameinfo"],
            data["timecreated"],
            data["timecreatedat"],
            data["location"],
            data["loccountrycode"],
            data["summary"],
            data["vac"],
            data["islimited"],
            data["mostplayedgamestotalplaytime"],
            data["mostplayedgames2weeksplaytime"],
            data["mostplayedgamesappids"],
            data["mostplayedgames"],
            data["mostplayedgamestimes"],
            data["friendsstate"],
            data["friendscount"],
            data["gamescount"],
            data["groupscount"],
            data["badgescount"],
            data["tradeban"],
            data["gameban"],
            data["lastbandays"],
            data["level"],
        )


@dataclass
class SteamIDResponse:
    __slots__ = ("steamid2", "steamid3", "steamid64")
    steamid2: str
    steamid3: str
    steamid64: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> SteamIDResponse:
        return cls(
            data["steamids"]["steamid2"],
            data["steamids"]["steamid3"],
            data["steamids"]["steamid64"],
        )


@dataclass
class SteamSale:
    __slots__ = ("price", "timestamp", "date")

    price: float
    timestamp: float
    date: datetime.datetime

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> SteamSale:
        return cls(
            data["price"],
            data["timestamp"],
            parse_timestamp(data["date"]),
        )


@dataclass
class StickerData:
    __slots__ = (
        "slot",
        "sticker_id",
        "wear",
        "scale",
        "rotation",
        "tint_id",
        "offset_x",
        "offset_y",
        "name",
        "image",
    )

    slot: int
    sticker_id: int
    wear: Optional[float]  # TODO: confirm
    scale: Optional[float]  # TODO: Confirm
    rotation: Optional[float]  # TODO: Confirm
    tint_id: Optional[float]  # TODO: Confirm
    offset_x: Optional[float]  # TODO: Confirm
    offset_y: Optional[float]  # TODO: Confirm
    name: str
    image: str

    @classmethod
    def _from_data(cls, data: Dict[str, Any]) -> StickerData:
        return cls(
            data["slot"],
            data["stickerid"],
            data.get("wear"),
            data.get("scale"),
            data.get("rotation"),
            data.get("tintid"),
            data.get("offsetx"),
            data.get("offsety"),
            data["name"],
            data["image"],
        )
