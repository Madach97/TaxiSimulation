from location import Location
"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """
    A rider

    ===============
    Attributes:
        @param str id: an identifier (or name) of the rider
        @param Location origin: the current location of the rider
        @param Location destination: the rider's destination
        @param str status: the status of the rider, which is one of - waiting,
                           cancelled, or satisfied
        @param int patience: the time the rider will wait before cancelling
    ================

    """
    def __init__(self, id, origin, destination, patience):
        """
        Create a new rider profile

        @param str id: identifier of rider
        @param Location origin: starting point of rider
        @param Location destination: destination of rider
        @param int patience: the time the rider will wait before cancelling
        @rtype: None

        """
        self.id = id
        self.origin = origin
        self.destination = destination
        self.patience = patience
        self.status = WAITING

    def __str__(self):
        """
        Return a string representation.

        @param Rider self: This rider
        @rtype: str

        >>> r = Rider("r1", Location(0,0), Location(3,4), 3)
        >>> print(r)
        r1
        """
        return str(self.id)

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @param Rider self: This rider
        @rtype: bool

        >>> r = Rider("r1", Location(0,0), Location(3,4), 3)
        >>> r1 = Rider("r1", Location(0,0), Location(3,4), 3)
        >>> r2 = Rider("r2", Location(3,0), Location(3,4), 3)
        >>> r == r1
        True
        >>> r == r2
        False
        >>> r == "r1"
        False
        """
        return (type(self) == type(other) and self.id == other.id and
                self.origin == other.origin and self.destination ==
                other.destination and self.patience == other.patience and
                self.status == other.status)
