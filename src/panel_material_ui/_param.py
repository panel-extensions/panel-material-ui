from __future__ import annotations

import datetime
from typing import Any

from param import CalendarDate as _CalendarDate
from param import Date as _Date


def to_date(value: Any) -> datetime.date:
    """
    Convert a value to a datetime.date.

    Arguments
    ----------
    value: Any
        The value to convert to a datetime.date.

    Returns
    -------
    datetime.date
        The converted value.

    Raises
    ------
    ValueError
        If the value could not be converted to a datetime.date.
    """
    if isinstance(value, str):
        value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    elif isinstance(value, datetime.datetime):
        value = value.date()
    elif hasattr(value, 'to_pydatetime'):
        value = value.to_pydatetime().date()
    if not isinstance(value, datetime.date):
        raise ValueError(f"Value {value} could not be converted to a datetime.date")
    return value


def to_datetime(value) -> datetime.datetime:
    """
    Convert a value to a datetime.datetime.

    Arguments
    ----------
    value: Any
        The value to convert to a datetime.datetime.

    Returns
    -------
    datetime.datetime
        The converted value.

    Raises
    ------
    ValueError
        If the value could not be converted to a datetime.datetime.
    """
    if isinstance(value, str):
        value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    elif isinstance(value, datetime.date):
        value = datetime.datetime.combine(value, datetime.datetime.min.time())
    elif hasattr(value, 'to_pydatetime'):
        value = value.to_pydatetime()
    if not isinstance(value, datetime.datetime):
        raise ValueError(f"Value {value} could not be converted to a datetime.datetime")
    return value


class Date(_CalendarDate):
    """
    The Date parameter is a parameter that allows the user to select a date.
    """

    def __init__(
        self,
        default: datetime.datetime | datetime.date | str | None = None,
        **params: Any
    ):
        default = self._parse_value(default)
        super().__init__(default=default, **params)

    def _parse_value(self, value: Any) -> Any:
        return to_date(value)

    def __set__(self, instance: Any, value: Any) -> None:
        value = self._parse_value(value)
        super().__set__(instance, value)


class Datetime(_Date):
    """
    The Datetime parameter is a parameter that allows the user to select a datetime.
    """

    def __init__(
        self,
        default: datetime.datetime | str | None = None,
        **params: Any
    ):
        default = self._parse_value(default)
        super().__init__(default=default, **params)

    def _parse_value(self, value: Any) -> Any:
        return to_datetime(value)

    def __set__(self, instance: Any, value: Any) -> None:
        value = self._parse_value(value)
        super().__set__(instance, value)
