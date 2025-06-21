from __future__ import annotations

import datetime
from typing import Any

import numpy as np
from param import CalendarDate as _CalendarDate
from param import Date as _Date
from param import List


def to_date(value: Any) -> datetime.date | None:
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
    if isinstance(value, np.datetime64):
        value = value.astype(datetime.date)
    if isinstance(value, str):
        value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    elif isinstance(value, datetime.datetime):
        value = value.date()
    elif hasattr(value, 'to_pydatetime'):
        value = value.to_pydatetime().date()
    if not isinstance(value, datetime.date) and value is not None:
        raise ValueError(f"Value {value} could not be converted to a datetime.date")
    return value


def to_datetime(value) -> datetime.datetime | None:
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
    if isinstance(value, np.datetime64):
        value = value.astype(datetime.datetime)
    if isinstance(value, str):
        if value.count(':') == 2:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        elif value.count(':') == 1:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
        else:
            value = datetime.datetime.strptime(value, "%Y-%m-%d")
    elif isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        value = datetime.datetime.combine(value, datetime.datetime.min.time())
    elif hasattr(value, 'to_pydatetime'):
        value = value.to_pydatetime()
    if not isinstance(value, datetime.datetime) and value is not None:
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

    def _parse_value(self, value: Any) -> datetime.date | None:
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

    def _parse_value(self, value: Any) -> datetime.datetime | None:
        return to_datetime(value)

    def __set__(self, instance: Any, value: Any) -> None:
        value = self._parse_value(value)
        super().__set__(instance, value)


class DateList(List):
    """
    The DateList parameter is a parameter that allows the user to select a list of dates.
    """

    def __init__(
        self,
        default: list[datetime.date] | list[datetime.datetime] | list[str] | None = None,
        **params: Any
    ):
        if default is None:
            default = []
        default = self._parse_value(default)
        super().__init__(default=default, **params)

    def _parse_value(self, value: Any) -> list[datetime.date] | None:
        return [to_date(v) for v in value]

    def __set__(self, instance: Any, value: Any) -> None:
        value = self._parse_value(value)
        super().__set__(instance, value)
