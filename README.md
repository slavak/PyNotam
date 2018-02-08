# PyNotam
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fslavak%2FPyNotam.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fslavak%2FPyNotam?ref=badge_shield)

**No**tice **T**o **A**ir**m**en Parser module written in Python.

This provides a means to parse standard format ICAO NOTAMs, and extract useful information from them without having to do any string processing yourself.

## Usage

Parsing a NOTAM is as easy as:

```python
>>> s = """(A1912/15 NOTAMN
Q) LOVV/QWPLW/IV/BO/W/000/130/4809N01610E001
A) LOVV B) 1509261100 C) 1509261230
E) PJE WILL TAKE PLACE AT AREA LAAB IN WALDE
PSN:N480930 E0161028 RADIUS - 1NM
F) GND G) FL130)"""
>>> n = notam.Notam.from_str(s)
```

Now you can access all information provided in the NOTAM easily and natively:

```python
>>> n.valid_from
datetime.datetime(2015, 9, 26, 11, 0, tzinfo=datetime.timezone.utc)
>>> n.area
{'lat': '4809N', 'long': '01610E', 'radius': 1}
```

You can also get a decoded form of the NOTAM, with all ICAO abbreviations expanded, with a single method call:

```python
>>> print(n.decoded())
(A1912/15 NOTAMN
Q) LOVV/QWPLW/IV/BO/W/000/130/4809N01610E001
A) LOVV B) 1509261100 C) 1509261230
E) Parachute Jumping Exercise WILL TAKE PLACE AT AREA LAAB IN WALDE
Position:N480930 E0161028 RADIUS - 1NM
F) Ground G) FL130
```

For a full list of the fields available in a Notam object, see its `__init__` method in the code.

## Requirements

Tested on Python 3.5.

Parsing grammar implemented with Erik Rose's excellent module [Parsimonious](https://github.com/erikrose/parsimonious). To install it:

```
> pip install parsimonious
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fslavak%2FPyNotam.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fslavak%2FPyNotam?ref=badge_large)