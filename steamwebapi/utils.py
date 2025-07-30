import datetime
from itertools import islice
from typing import Dict, Generator, Iterable, List, Tuple, TypeVar, Union

__all__ = ("utcnow", "as_chunks")

T = TypeVar("T")

_JSONPrimitive = Union[None, bool, str, float, int]
JSON = Union[_JSONPrimitive, List["JSON"], Dict[str, "JSON"]]


def parse_timestamp(ts_string: str, /) -> datetime.datetime:
    """Parses a string to an aware UTC datetime."""
    return datetime.datetime.strptime(ts_string, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=datetime.timezone.utc)


def parse_date(date_string: str, /) -> datetime.datetime:
    """
    Parses a string containing a date to a datetime.

    For comparison reasons, the resulting object will have a UTC timezone.
    """
    return datetime.datetime.strptime(date_string, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)


def parse_iso_utc_timestamp(ts_string: str, /) -> datetime.datetime:
    """Parses an ISO format string to an aware UTC datetime."""
    return datetime.datetime.strptime(ts_string, "%Y-%m-%dT%H:%M:%S.%f+00:00")


def to_iso_format(dt: datetime.datetime, /) -> str:
    """Transforms a datetime.datetime to an ISO string."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def utcnow() -> datetime.datetime:
    """Returns an aware UTC datetime representing the current time.

    Returns
    --------
    :class:`datetime.datetime`
        The current time in UTC as an aware datetime.
    """
    return datetime.datetime.now(datetime.timezone.utc)


def as_chunks(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
    """Batches an iterable into chunks of up to size n.

    Parameters
    ----------
    iterable: :class:`collections.abc.Iterable`
        The iterable to batch
    n: :class:`int`
        The number of elements per generated tuple.

    Raises
    ------
    :class:`ValueError`
        At least one result must be returned per group.
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch
