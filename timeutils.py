from datetime import *


class EstimatedDateTime(datetime):
    """Represents an estimated point in time. Instances are identical to datetime.datetime in every way,
    except that the instance will have an attribute 'is_estimated' which is set to True."""

    def __new__(cls, *args, **kwargs):
        """May be initialized either identically to a regular datetime.datetime or, optionally, by
        providing an existing datetime object to copy."""

        if not kwargs and len(args)==1 and isinstance(args[0], datetime):
            other = args[0]
            v = super().__new__(cls, other.year, other.month, other.day,
                                     other.hour, other.minute, other.second,
                                     other.microsecond, other.tzinfo)
        else:
            v = super().__new__(cls, *args, **kwargs)
        v.is_estimated = True
        return v