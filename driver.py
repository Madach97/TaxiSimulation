from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """
        Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.id, self.location, self._speed = identifier, location, int(speed)
        self.is_idle = True
        self._destination = None

    def __str__(self):
        """
        Return a string representation.

        @type self: Driver
        @rtype: str

        >>> d = Driver("d1", Location(0,4), 12)
        >>> print(d)
        d1
        """
        return str(self.id)

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool

        >>> d = Driver("d1", Location(0,4), 10)
        >>> d1 = Driver("d1", Location(0,4), 10)
        >>> d2 = Driver("d2", Location(0,4), 10)
        >>> d == d1
        True
        >>> d == d2
        False
        >>> d == "d1"
        False
        """
        return (type(self) == type(other) and self.id == other.id and
                self.location == other.location and self.is_idle ==
                other.is_idle)

    def get_travel_time(self, destination):
        """
        Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> loc = Location(5,5)
        >>> d = Driver("Bob", Location(5,5), 10)
        >>> time = d.get_travel_time(Location(10,10))
        >>> print(time)
        1
        >>> type(time) == int
        True
        """
        return int(manhattan_distance(self.location, destination) / self._speed)

    def start_drive(self, location):
        """
        Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int

        >>> d = Driver("d1", Location(0,4), 10)
        >>> time = d.start_drive(Location(9,5))
        >>> print(time)
        1
        >>> print(d._destination)
        9,5
        """
        self._destination = location
        return self.get_travel_time(location)

    def end_drive(self):
        """
        End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> d = Driver("d1", Location(0,4), 10)
        >>> d._destination = Location(9,4)
        >>> print(d._destination)
        9,4
        >>> d.end_drive()
        >>> d.location == d._destination
        False
        >>> print(d.location)
        9,4
        >>> print(d._destination)
        None
        >>> d.is_idle
        True
        """
        self.location = self._destination
        self._destination = None
        self.is_idle = True

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> d = Driver("d1", Location(0,4), 10)
        >>> r = Rider("r", Location(0,0), Location(9,1), 12)
        >>> time = d.start_ride(r)
        >>> d.location == d._destination
        False
        >>> print(d.location)
        0,4
        >>> d._destination == r.destination
        True
        >>> d.is_idle
        False
        >>> print(time)
        1
        """
        self.is_idle = False
        self._destination = rider.destination
        return self.get_travel_time(rider.destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> d = Driver("d1", Location(0,4), 10)
        >>> d._destination = Location(9,4)
        >>> print(d._destination)
        9,4
        >>> d.end_ride()
        >>> print(d.location)
        9,4
        >>> print(d._destination)
        None
        >>> d.is_idle
        True

        """
        self.location = self._destination
        self.is_idle = True
        self._destination = None
