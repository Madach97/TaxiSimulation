class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        self.row = int(row)
        self.column = int(column)

    def __str__(self):
        """
        Return a string representation.

        @rtype: str

        >>> print(Location(2,4))
        2,4
        """
        return "{},{}".format(self.row, self.column)

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @rtype: bool

        >>> Location(3,4) == Location(3,4)
        True
        >>> Location(3,4) == "3,4"
        False
        >>> Location(4,5) == Location(9,16)
        False
        """
        return (type(self) == type(other) and self.row == other.row and
                self.column == other.column)


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    >>> org = Location(2,3)
    >>> loc = Location(1,1)
    >>> manhattan_distance(org, loc)
    3
    >>> manhattan_distance(Location(0,0), Location(5,7))
    12
    >>> manhattan_distance(Location(3,4), Location(3,4))
    0
    """
    return abs(destination.row - origin.row) + abs(destination.column -
                                                   origin.column)


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> loc2 = Location(9,8)
    >>> dest = deserialize_location("9,8")
    >>> print(str(dest.row))
    9
    >>> print(str(dest.column))
    8

    """
    loc = location_str.split(",")   # splits the str where there is comma
    return Location(int(loc[0]), int(loc[1]))
