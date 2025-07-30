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
from types import TracebackType
from typing import TYPE_CHECKING, List, Mapping, Optional, Sequence, Type, Union

from .enums import (
    Game,
    InventoryState,
    ItemGroup,
    ItemHistoryOrigin,
    ItemHistorySource,
    ItemHistoryType,
    ItemType,
    Language,
    ScreenshotColorScheme,
    ScreenshotFormat,
    ScreenshotLogoOffset,
    SortOrder,
    Wear,
)
from .http import HTTPClient, Route
from .models import (
    AccountInformation,
    ExchangeRates,
    FloatData,
    InventoryHistoryEntry,
    InventoryItem,
    Item,
    ItemAutocompleteResult,
    ItemHistoryEntry,
    Profile,
    SteamIDResponse,
)
from .steamid import SteamID

if TYPE_CHECKING:
    from typing_extensions import Self


class Client:
    """A SteamWebAPI client.

    .. container:: operations

        .. describe:: async with x:

            Returns the client itself. Used to gracefully close the client on exit.

            .. code-block:: python3

                async with steamwebapi.Client(token) as client:
                    ...
    """

    def __init__(self, token: str, production: bool = True):
        """Creates a new client.

        Parameters
        ----------
        token: :class:`str`
            Your SteamWebAPI token.
        production: :class:`bool`
            Whether to run in production mode, defaults to True.
        """
        self.http = HTTPClient(token, production)

    async def get_account_information(self) -> AccountInformation:
        """|coro|

        Retrieve information about your SteamWebAPI account.

        Returns
        -------
        :class:`~steamwebapi.models.AccountInformation`
            Your account information.

        Raises
        ------
        TODO: steamwebapi errors.
        """
        r = Route("GET", "/account/me")
        data = await self.http.request(r)
        return AccountInformation._from_data(data)

    # NOTE/TODO: This accepts a "state" parameter to make faster requests that return less data.. Maybe worth exposing.
    async def get_profile(
        self,
        steam_id: Union[SteamID, str],
        no_cache: Optional[bool] = None,
        force_from_db_if_exists: Optional[bool] = None,
    ) -> Profile:
        """|coro|

        Retrieve a steam profile.

        Parameters
        ----------
        steam_id: Union[:class:`~steamwebapi.steamid.SteamID`, :class:`str`]
            The SteamID, profile url, or username to retrieve a profile for.
        no_cache: Optional[:class:`bool`]
            Whether to use a cached profile, if possible.
        force_from_db_if_exists: Optional[:class:`bool`]
            TODO: I don't know....

        Returns
        -------
        :class:`~steamwebapi.models.Profile`
            The requested profile.

        Raises
        ------
        TODO: steamwebapi errors.
        """
        # NOTE: steam_id can be a steam id, profile url, or username
        params = {"id": str(steam_id)}

        if no_cache is not None:
            params["no_cache"] = "true" if no_cache else "false"
        if force_from_db_if_exists is not None:
            params["force_from_db_if_exists"] = "1" if force_from_db_if_exists else "0"

        r = Route("GET", "/steam/api/profile")
        data = await self.http.request(r, params=params)
        return Profile._from_data(data)

    # NOTE/TODO: This accepts a "state" parameter to make faster requests that return less data.. Maybe worth exposing.
    async def get_profiles(self, *steam_id: SteamID) -> List[Profile]:
        """|coro|

        Retrieve up to 20 profiles at a time.

        Parameters
        ----------
        *steam_id: :class:`~steamwebapi.steamid.SteamID`
            The steam ids to retrieve the profiles of.

        Returns
        -------
        List[:class:`~steamwebapi.models.Profile`]
            The requested profiles.

        Raises
        ------
        :class:`ValueError`
            Invalid number of steam ids provided.
        TODO: steamwebapi errors.
        """
        # NOTE: This only accepts steamid64s
        if not 0 < len(steam_id) <= 20:
            raise ValueError("you can only retrieve 20 profiles at a time.")

        params = {"id": ",".join(str(id_) for id_ in steam_id)}

        r = Route("GET", "/steam/api/profile/batch")
        data = await self.http.request(r, params=params)
        return [Profile._from_data(sub) for sub in data]

    async def get_items(
        self,
        game: Game = Game.CS2,
        page: int = 1,
        max: int = 50_000,
        sort_by: Optional[SortOrder] = None,
        search: Optional[str] = None,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        price_real_min: Optional[int] = None,
        price_real_max: Optional[int] = None,
        item_group: Optional[ItemGroup] = None,
        item_type: Optional[ItemType] = None,
        item_name: Optional[str] = None,
        wear: Optional[Union[Wear, Sequence[Wear]]] = None,
    ) -> List[Item]:  # This is not accurate, should be an Item instead.
        params = {
            "game": game.value,
            "page": page,
            "max": max,
        }

        if sort_by is not None:
            params["sort_by"] = sort_by.value
        if search is not None:
            params["search"] = search
        if price_min is not None:
            params["price_min"] = price_min
        if price_max is not None:
            params["price_max"] = price_max
        if price_real_min is not None:
            params["price_real_min"] = price_real_min
        if price_real_max is not None:
            params["price_real_max"] = price_real_max
        if item_group is not None:
            params["item_group"] = item_group.value
        if item_type is not None:
            params["item_type"] = item_type.value
        if item_name is not None:
            params["item_name"] = item_name
        if wear is not None:
            params["wear"] = ",".join(w.value for w in wear) if isinstance(wear, Sequence) else wear.value

        r = Route("GET", "/steam/api/items")
        data = await self.http.request(r, params=params)
        return [Item._from_data(d) for d in data]

    def _handle_inventory_params(
        self,
        steam_ids: Optional[Sequence[SteamID]] = None,
        steam_id: Optional[SteamID] = None,
        game: Game = Game.CS2,
        parse: Optional[bool] = None,
        language: Optional[Language] = None,
        no_cache: Optional[bool] = None,
        group: Optional[bool] = None,
        state: Optional[InventoryState] = None,
        with_no_tradeable: Optional[bool] = None,
        steam_login_secure: Optional[str] = None,
        trade_url: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        with_floats: Optional[bool] = None,
        try_first_seven_days_blocked_items: Optional[bool] = None,
        currency: Optional[str] = None,
        sort: Optional[SortOrder] = None,
    ) -> Mapping[str, str]:  # TODO: Unnecessary Any...

        if steam_ids is not None and (steam_id is not None or trade_url is not None):
            raise ValueError("steam_ids cannot be combined with steam_id or trade_url parameters")

        params = {"game": game.value}

        if steam_id is not None:
            params["steam_id"] = str(steam_id)  # TODO: Fix this to use a SteamID object.
        if steam_ids is not None:
            params["steam_ids"] = ",".join(str(id_) for id_ in steam_ids)
        if parse is not None:
            params["parse"] = "true" if parse else "false"
        if language is not None:
            params["language"] = language.value
        if no_cache is not None:
            params["no_cache"] = "true" if no_cache else "false"
        if group is not None:
            params["group"] = "true" if group else "false"
        if state is not None:
            params["state"] = state.value
        if with_no_tradeable is not None:
            params["with_no_tradeable"] = "true" if with_no_tradeable else "false"
        if steam_login_secure is not None:
            params["steam_login_secure"] = steam_login_secure
        if trade_url is not None:
            params["trade_url"] = trade_url
        if offset is not None:
            params["offset"] = str(offset)
        if limit is not None:
            params["limit"] = str(limit)
        if with_floats is not None:
            params["with_floats"] = "true" if with_floats else "false"
        if try_first_seven_days_blocked_items is not None:
            params["try_first_seven_days_blocked_items"] = "true" if try_first_seven_days_blocked_items else "false"
        if currency is not None:
            params["currency"] = currency
        if sort is not None:
            params["sort"] = sort.value

        return params

    async def get_inventory(
        self,
        steam_id: Optional[SteamID] = None,
        game: Game = Game.CS2,
        parse: Optional[bool] = None,
        language: Optional[Language] = None,
        no_cache: Optional[bool] = None,
        group: Optional[bool] = None,
        state: Optional[InventoryState] = None,
        with_no_tradeable: Optional[bool] = None,
        steam_login_secure: Optional[str] = None,
        trade_url: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        with_floats: Optional[bool] = None,
        try_first_seven_days_blocked_items: Optional[bool] = None,
        currency: Optional[str] = None,
        sort: Optional[SortOrder] = None,
    ) -> List[InventoryItem]:

        if steam_id is None and trade_url is None:
            raise ValueError("must provide steam_id or trade_url.")

        params = self._handle_inventory_params(
            steam_id=steam_id,
            game=game,
            parse=parse,
            language=language,
            no_cache=no_cache,
            group=group,
            state=state,
            with_no_tradeable=with_no_tradeable,
            steam_login_secure=steam_login_secure,
            trade_url=trade_url,
            offset=offset,
            limit=limit,
            with_floats=with_floats,
            try_first_seven_days_blocked_items=try_first_seven_days_blocked_items,
            currency=currency,
            sort=sort,
        )

        r = Route("GET", "/steam/api/inventory")
        data = await self.http.request(r, params=params)
        return [InventoryItem._from_data(sub) for sub in data]

    async def get_inventories(
        self,
        *steam_ids: SteamID,
        game: Game = Game.CS2,
        parse: Optional[bool] = None,
        language: Optional[Language] = None,
        no_cache: Optional[bool] = None,
        group: Optional[bool] = None,
        state: Optional[InventoryState] = None,
        with_no_tradeable: Optional[bool] = None,
        steam_login_secure: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        with_floats: Optional[bool] = None,
        try_first_seven_days_blocked_items: Optional[bool] = None,
        currency: Optional[str] = None,
        sort: Optional[SortOrder] = None,
    ) -> Mapping[str, List[InventoryItem]]:
        if not 0 < len(steam_ids) <= 20:
            raise ValueError("you must provide at least one and no more than 20 steam ids.")

        params = self._handle_inventory_params(
            steam_ids=steam_ids,
            game=game,
            parse=parse,
            language=language,
            no_cache=no_cache,
            group=group,
            state=state,
            with_no_tradeable=with_no_tradeable,
            steam_login_secure=steam_login_secure,
            offset=offset,
            limit=limit,
            with_floats=with_floats,
            try_first_seven_days_blocked_items=try_first_seven_days_blocked_items,
            currency=currency,
            sort=sort,
        )

        r = Route("GET", "/steam/api/inventory/batch")
        data = await self.http.request(r, params=params)
        return {steam_id: [InventoryItem._from_data(sub) for sub in inventory] for steam_id, inventory in data.items()}

    async def get_inventory_history(self, steam_id: SteamID, game: Game = Game.CS2) -> List[InventoryHistoryEntry]:
        params = {"steam_id": str(steam_id), "game": game.value}  # TODO: Fix steam_id to use a SteamID object

        r = Route("GET", "/steam/api/inventory/history")
        data = await self.http.request(r, params=params)
        return [InventoryHistoryEntry._from_data(sub) for sub in data]

    async def get_item_info(
        self,
        market_hash_name: str,
        currency: Optional[str] = None,
        with_groups: Optional[bool] = None,
    ) -> Item:  # TODO: Fix this return type
        params = {
            "market_hash_name": market_hash_name,
        }

        if currency is not None:
            params["currency"] = currency
        if with_groups is not None:
            params["with_groups"] = "true" if with_groups else "false"

        r = Route("GET", "/steam/api/item")
        data = await self.http.request(r, params=params)
        return Item._from_data(data)

    async def get_item_history(
        self,
        market_hash_name: str,
        origin: Optional[ItemHistoryOrigin] = None,
        type: Optional[ItemHistoryType] = None,
        source: Optional[ItemHistorySource] = None,  # TODO: get list of options
        interval: Optional[int] = None,  # TODO: Get valid limits?
        start_date: Optional[Union[datetime.date, datetime.datetime]] = None,
        end_date: Optional[Union[datetime.date, datetime.datetime]] = None,
    ) -> List[ItemHistoryEntry]:
        """|coro|

        Retrieve history for an item.

        Parameters
        ----------
        market_hash_name: class:`str`
            The market hash name of the item.
        origin: Optional[:class:`~steamwebapi.enums.ItemHistoryOrigin`]
            Where to retrieve historical item data from.
        type: Optional[:class:`~steamwebapi.enums.ItemHistoryType`]
            What type of historical information to receive.
        source: Optional[:class:`~steamwebapi.enums.ItemHistorySource`]
            Where to retrieve the item history from.
        interval: Optional[:class:`int`]
            What interval to retrieve prices in ### TODO: need to know what the unit is and what the valid limits are.
        start_date: Optional[Union[:class:`datetime.date`, :class:`datetime.datetime`]]
            Starting date for filtering by date, if given.
        end_date: Optional[Union[:class:`datetime.date`, :class:`datetime.datetime`]]
            End date for filtering by date, if given.

        Returns
        -------
        List[:class:`~steamwebapi.models.ItemHistoryEntry`]
            The requested item history.

        Raises
        ------
        :class:`ValueError`
            ``source`` can only be ``skinport`` if ``type`` is ``offer``
        TODO: steamwebapi errors
        """

        if (source is not None and source is ItemHistorySource.skinport) and type is not ItemHistoryType.offer:
            raise ValueError("skinport source can only be used if the type parameter is offer.")

        params = {"market_hash_name": market_hash_name}

        if origin is not None:
            params["origin"] = origin.value
        if type is not None:
            params["type"] = type.value
        if source is not None:
            params["source"] = source.value
        if interval is not None:
            params["interval"] = str(interval)
        if start_date is not None:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date is not None:
            params["end_date"] = end_date.strftime("%Y-%m-%d")

        r = Route("GET", "/steam/api/history")
        data = await self.http.request(r, params=params)
        return [ItemHistoryEntry._from_data(sub) for sub in data]

    async def get_float_info(self, inspect_link: str) -> FloatData:
        """|coro|

        Retrieve float information for an item using its inspect link.

        Parameters
        ----------
        inspect_link: :class:`str`
            The inspect link of the item.

        Returns
        -------
        :class:`~steamwebapi.models.FloatData`
            The requested float data.

        Raises
        ------
        TODO: steamwebapi errors
        """
        params = {"url": inspect_link}

        r = Route("GET", "/steam/api/float")
        data = await self.http.request(r, params=params)
        return FloatData._from_data(data)

    async def get_screenshot(
        self,
        inspect_link: str,
        as_base64: bool = False,  # TODO: overloads for this?
        color: Optional[ScreenshotColorScheme] = None,
        background_url: Optional[str] = None,
        logo_url: Optional[str] = None,
        logo_offset_start: Optional[ScreenshotLogoOffset] = None,
        logo_offset_x: Optional[int] = None,
        logo_offset_y: Optional[int] = None,
        logo_opacity: Optional[float] = None,
        logo_width: Optional[int] = None,
        format: Optional[ScreenshotFormat] = None,  # TODO: Does this need overloads too?
    ) -> Union[bytes, str]:
        """|coro|

        Retrieve a screenshot of an item using its inspect link.

        Parameters
        ----------
        inspect_link: :class:`str`
            The inspect link of the item.
        as_base64: :class:`bool`
            Whether to return base64 encoded data, by default False
        color: Optional[:class:`~steamwebapi.enums.ScreenshotColorScheme`]
            The color scheme for the screenshot.
        background_url: Optional[:class:`str`]
            A url to an image to be used as the background.
        logo_url: Optional[:class:`str`]
            A url to an image to be used as a logo.
        logo_offset_start: Optional[:class:`~steamwebapi.enums.ScreenshotLogoOffset`]
            Anchor point for the logo.
        logo_offset_x: Optional[:class:`int`]
            Logo X offset.
        logo_offset_y: Optional[:class:`int`]
            Logo Y offset.
        logo_opacity: Optional[:class:`float`]
            Logo opacity. Must be (0.0, opacity, 1.0]
        logo_width: Optional[:class:`int`]
            Logo width. Must be (0, width, 500]
        format: Optional[:class:`~steamwebapi.enums.ScreenshotFormat`]
            The format for the resulting screenshot.

        Returns
        -------
        Union[:class:`bytes`, :class:`str`]
            The resulting screenshot in ``PNG`` format, either as bytes or base64 encoded to a string.

        Raises
        ------
        :class:`ValueError`
            Invalid logo opacity or logo width provided.
        TODO: steamwebapi errors.
        """
        # NOTE: returns a PNG format image.
        if logo_opacity is not None and (logo_opacity > 1.0 or logo_opacity < 0):
            raise ValueError("logo opacity must be in 0.0 < x <= 1.0")

        if logo_width is not None and (logo_width < 0 or logo_width > 500):
            raise ValueError("logo width must be 0 < width <= 500")

        params = {
            "url": inspect_link,
            "as_base64": "1" if as_base64 else "0",  # TODO: maybe make this nullable?
        }

        if color is not None:
            params["color"] = color.value
        if background_url is not None:
            params["background_url"] = background_url
        if logo_url is not None:
            params["logo_url"] = logo_url
        if logo_offset_start is not None:
            params["logo_offset_start"] = logo_offset_start.value
        if logo_offset_x is not None:
            params["logo_offset_x"] = str(logo_offset_x)
        if logo_offset_y is not None:
            params["logo_offset_y"] = str(logo_offset_y)
        if logo_width is not None:
            params["logo_width"] = str(logo_width)
        if format is not None:
            params["format"] = format.value

        r = Route("GET", "/steam/api/float/screenshot")
        data = await self.http.request(r, params=params)
        return data

    async def autocomplete_item_name(self, search: str, game: Game = Game.CS2) -> List[ItemAutocompleteResult]:
        """|coro|

        Retrieve autocompletions for an item name search.

        Parameters
        ----------
        search: :class:`str`
            The current search term.
        game: :class:`~steamwebapi.enums.Game`
            The game to search items for, cs2 by default.

        Returns
        -------
        List[:class:`~steamwebapi.models.ItemAutocompleteResult`]
            Autocompletion results.

        Raises
        ------
        TODO: steamwebapi errors.
        """
        params = {"search": search, "game": game.value}

        r = Route("GET", "/steam/api/complete/items")
        data = await self.http.request(r, params=params)
        return [ItemAutocompleteResult._from_data(sub) for sub in data]

    async def convert_steam_id(self, steam_id: str) -> SteamIDResponse:
        """|coro|

        Convert a steam id between different formats.

        The api currently supports:
            - SteamID2
            - SteamID3
            - SteamID64

        .. note::

            This method makes an api call. For local conversion, see :class:`~steamwebapi.steamid.SteamID`
            for locally processed conversions instead.

        Parameters
        ----------
        steam_id: :class:`str`
            The id to convert.

        Returns
        -------
        :class:`~steamwebapi.models.SteamIDResponse`
            The api response.

        Raises
        ------
        TODO: steamwebapi errors
        """
        params = {"steam_id": steam_id}

        r = Route("GET", "/steam/api/info/steamid")
        data = await self.http.request(r, params=params)
        return SteamIDResponse._from_data(data)

    async def get_exchange_rates(self, base: str = "USD", source: str = "Steam") -> ExchangeRates:
        """|coro|

        Retrieve exchange rates for various currencies and cryptos.

        Parameters
        ----------
        base: :class:`str`
            ISO 4217 currency code to use as the base rate. Defaults to USD.
        source: :class:`str`
            The source of the exchange rates, Steam by default.

        Returns
        -------
        :class:`~steamwebapi.models.ExchangeRates`
            The resulting exchange rates.

        Raises
        ------
        TODO: steamwebapi
        """
        params = {"base": base, "source": source}

        r = Route("GET", "/currency/api/list")
        data = await self.http.request(r, params=params)
        return ExchangeRates._from_data(data)

    async def exchange_currency(self, to: str, base: str = "USD") -> float:
        """|coro|

        Exchange one currency to another. For bulk usage, consider :meth:`get_exchange_rates` instead.

        Parameters
        ----------
        to: :class:`str`
            The ISO 4217 currency code to exchange to.
        base: :class:`str`
            The ISO 4217 currency code to exchange from. Defaults to "USD".

        Returns
        -------
        :class:`float`
            The exchange ratio of ``base : to``.

        Raises
        ------
        TODO: steamwebapi
        """
        params = {"change": to, "base": base}

        r = Route("GET", "/currency/api/exchange")
        data = await self.http.request(r, params=params)
        return data["changeRate"]

    def is_production_mode(self) -> bool:
        """
        Whether the client is running in production mode.

        Returns
        -------
        :class:`bool`
            ``True`` if running in production, ``False`` otherwise.
        """
        return self.http.production

    async def close(self) -> None:
        """|coro|

        Gracefully close the client.
        """
        await self.http.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()
