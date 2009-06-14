#!/usr/bin/env python

from datetime import datetime, timedelta, tzinfo
from operator import itemgetter

class DecodeError(Exception):
    pass


class TAI64DecodeError(DecodeError):
    pass


def decode_tai64n(hexdec, basedate=datetime(1970, 1, 1)):
    """ returns a datetime (TAI, not UTC!) object from tai64 string
    
        Example
            >>> # (from http://cr.yp.to.mirror.dogmap.org/libtai/tai64.html)
            >>> decode_tai64n("400000002a2b2c2d")
            datetime.datetime(1992, 6, 2, 8, 7, 9)
            >>> # a more recent one
            >>> decode_tai64n("400000004a32392b2aa21dac")
            datetime.datetime(2009, 6, 12, 11, 16, 59, 715267)
    """
    try:
        nano_hex = (len(hexdec) == 24) and hexdec[16:24]
    except IndexError:
        pass
    try:
        tai_int = int(hexdec[0:16], 16)
        nano_int = nano_hex and int(nano_hex, 16)
    except:
        raise TAI64DecodeError("'%s' not a valid hex value." % hexdec)
    # we decode only after 01.01.1970
    seconds = tai_int - 4611686018427387904L
    if seconds < 0:
        raise TAI64DecodeError("I won't decode gone millenia "
                               "(i.e. nothing prior to 01.01.1970).")
    return basedate + timedelta(0, seconds, nano_int/1000)


def __conversion_table():
    """ returns [datetime, value] where value == seconds between TAI and UTC
    
    Example:
    >>> __conversion_table()[-1]
    (datetime.datetime(1972, 1, 1, 0, 0), 10.0)
    """
    # update this table as new values become known
    # source: ftp://maia.usno.navy.mil/ser7/tai-utc.dat
    conversion_table = [(datetime(1972, 01,  1), 10.0),
                        (datetime(1972, 07,  1), 11.0),
                        (datetime(1973, 01,  1), 12.0),
                        (datetime(1974, 01,  1), 13.0),
                        (datetime(1975, 01,  1), 14.0),
                        (datetime(1976, 01,  1), 15.0),
                        (datetime(1977, 01,  1), 16.0),
                        (datetime(1978, 01,  1), 17.0),
                        (datetime(1979, 01,  1), 18.0),
                        (datetime(1980, 01,  1), 19.0),
                        (datetime(1981, 07,  1), 20.0),
                        (datetime(1982, 07,  1), 21.0),
                        (datetime(1983, 07,  1), 22.0),
                        (datetime(1985, 07,  1), 23.0),
                        (datetime(1988, 01,  1), 24.0),
                        (datetime(1990, 01,  1), 25.0),
                        (datetime(1991, 01,  1), 26.0),
                        (datetime(1992, 07,  1), 27.0),
                        (datetime(1993, 07,  1), 28.0),
                        (datetime(1994, 07,  1), 29.0),
                        (datetime(1996, 01,  1), 30.0),
                        (datetime(1997, 07,  1), 31.0),
                        (datetime(1999, 01,  1), 32.0),
                        (datetime(2006, 01,  1), 33.0),
                        (datetime(2009, 01,  1), 34.0),
                        # add new values here
                       ]
    conversion_table.sort(key=itemgetter(0), reverse=True)
    return conversion_table

def __tai_seconds(date, table=__conversion_table()):
    """ returns seconds of TAI-offset from UTC at date given.
        Works only on dates later than 01.01.1972.
    
    Example:
        >>> __tai_seconds(datetime(1992, 6, 2, 8, 7, 9))
        26.0
        >>> __tai_seconds(datetime(1971, 6, 2, 8, 7, 9))
        False
    """
    for x in table:
        if date > x[0]:
            return x[1]
    return False


def tai2utc(date):
    """ converts datetime.datetime TAI to datetime.datetime UTC.
        Works only on dates later than 01.01.1972.
    
    Example
        >>> tai2utc(datetime(1992, 6, 2, 8, 7, 9))
        datetime.datetime(1992, 6, 2, 8, 6, 43)
    """
    seconds = __tai_seconds(date)
    return seconds and (date - timedelta(0, seconds))


def utc2tai(date):
    """ converts datetime.datetime UTC to datetime.datetime TAI.
        Works only on dates later than 01.01.1972.

    Example
        >>> utc2tai(datetime(1992, 6, 2, 8, 6, 43))
        datetime.datetime(1992, 6, 2, 8, 7, 9)
    """
    seconds = __tai_seconds(date)
    return seconds and (date + timedelta(0, seconds))


if __name__ == '__main__':
    import doctest
    doctest.testmod()


