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

import re
from typing import Union

__all__ = ("SteamID",)

STEAMID64_MAGIC_NUMBER = 76561197960265728
STEAMID_PATTERN = re.compile(r"STEAM_[0-5]:[0-1]:\d+", re.IGNORECASE)
STEAMID3_PATTERN = re.compile(r"\[U:1:(\d+)\]", re.IGNORECASE)


class SteamID:
    """
    Wraps the value of Steam identifiers of different formats to allow the various formats to be used
    where only a single format may be permissible.

    This can also be used to convert one Steam ID format to another.

    Supported formats:
        - SteamID64
        - SteamID3
        - SteamID
        - Account ID

    .. container:: operations

        .. describe:: str(x)

            Returns the SteamID64 value as a string.

        .. describe:: int(x)

            Returns the SteamID64 value as an integer.

    Attributes
    ----------
    value: :class:`int`
        The SteamID64 value of this SteamID.
    """

    __slots__ = ("value",)

    def __init__(self, value: Union[str, int]):
        self.value: int = 0
        if isinstance(value, int):
            # Check if steamid64
            if 32 < value.bit_length() <= 64:
                self.value = value
            elif value.bit_length() <= 32:
                self.value = value + STEAMID64_MAGIC_NUMBER
            else:
                raise ValueError("invalid integer provided for value.")

        elif isinstance(value, str):
            if STEAMID_PATTERN.match(value) is not None:
                self.value = self._steamid_to_steamid64(value)
            elif (match := STEAMID3_PATTERN.match(value)) is not None:
                # transform into steamid64
                self.value = self._steamid3_to_steamid64(match)
            # Could be just a plain old string with a steamid64 in it
            elif len(value) == 17 and value.isnumeric():
                self.value = int(value)
            else:
                raise ValueError("invalid string provided for value.")

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value

    def __repr__(self):
        return f"<SteamID value={self.value}>"

    def _steamid_to_steamid64(self, val: str) -> int:
        parts = val.split(":")

        if len(parts) != 3 or not parts[2].isdigit():
            raise ValueError("invalid steamid given.")

        Y = int(parts[1])
        Z = int(parts[2])

        return STEAMID64_MAGIC_NUMBER + Z * 2 + Y

    def _steamid64_to_steamid(self, val: int) -> str:
        acc_id = val - STEAMID64_MAGIC_NUMBER
        Z, Y = divmod(acc_id, 2)

        return f"STEAM_1:{Y}:{Z}"

    def _steamid3_to_steamid64(self, match: re.Match) -> int:
        acc_id = match.group(1)

        return STEAMID64_MAGIC_NUMBER + int(acc_id)

    def _steamid64_to_steamid3(self, val: int) -> str:
        acc_id = val - STEAMID64_MAGIC_NUMBER

        return f"[U:1:{acc_id}]"

    def as_account_id(self) -> int:
        """Returns a :class:`int` representing the account id of this SteamID."""
        return self.value - STEAMID64_MAGIC_NUMBER

    def as_steamid(self) -> str:
        """Returns a :class:`str` representing the value of this SteamID in SteamID format."""
        return self._steamid64_to_steamid(self.value)

    def as_steamid3(self) -> str:
        """Returns a :class:`str` representing the value of this SteamID in SteamID3 format."""
        return self._steamid64_to_steamid3(self.value)

    def as_steamid64(self) -> int:
        """Returns a :class:`int` representing the value of this SteamID in SteamID64 format."""
        return self.value
