"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import *
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> dr = DriverRequest( 11, Driver("d1", Location(0,4), 10))
        >>> disp = Dispatcher()
        >>> mon = Monitor()
        >>> events = dr.do(disp, mon)
        >>> len(events) == 0
        True
        >>> rr = RiderRequest(10, Rider("r1", Location(0,0), Location(3,4), 4))
        >>> events = rr.do(disp, mon)
        >>> len(events) == 2
        True
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)
        print(self)
        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider,
                                 driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str

        >>> loc = Location(0,0)
        >>> loc1 = Location(3,4)
        >>> print(RiderRequest(10, Rider("r1", loc, loc1, 4)))
        10 -- r1: Request a driver

        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> disp = Dispatcher()
        >>> mon = Monitor()
        >>> rr = RiderRequest(10, Rider("r1", Location(0,0), Location(3,4), 4))
        >>> events = rr.do(disp, mon)
        >>> len(events) == 1
        True
        >>> dr = DriverRequest( 11, Driver("d1", Location(0,4), 10))
        >>> events = dr.do(disp, mon)
        >>> len(events) == 1
        True
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.

        monitor.notify(self.timestamp, DRIVER, REQUEST, self.driver.id,
                       self.driver.location)
        print(self)
        events = []

        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(
                    Pickup(self.timestamp + travel_time, rider, self.driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str

        >>> print(DriverRequest( 11, Driver("d1", Location(0,4), 10)))
        11 -- d1: Request a rider
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """
    Pickup for a rider is cancelled
    ==========
    Attributes:
        @param Rider rider: rider whose pickup is to be cancelled
    ===========

    """

    def __init__(self, timestamp, rider):
        """
        Create a cancellation event

        Extended from Event

        @param int timestamp: the event's timestamp
        @param Rider rider: the rider who requests a cancellation
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """
        Cancel the ride

        Overrides Event.do()

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> disp = Dispatcher()
        >>> mon = Monitor()
        >>> r = Rider("r1", Location(0,0), Location(3,4), 4)
        >>> cr = Cancellation( 10, r)
        >>> events = cr.do(disp, mon)
        >>> len(events) == 0
        True
        >>> r.status == CANCELLED
        True
        """
        # if the rider is not already picked up(or satisfied), then:
        # Notify the monitor about the request.
        # set the rider's status to cancelled
        # Ask dispatcher to cancel the ride

        events = []
        print(self)
        if not self.rider.status == SATISFIED:
            print(self)
            monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id,
                           self.rider.origin)
            self.rider.status = CANCELLED
            dispatcher.cancel_ride(self.rider)

        return events

    def __str__(self):
        """Return a string representation of this event.

        Overrides Event.__str__()

        @type self: Cancellation
        @rtype: str

        >>> loc = Location(0,0)
        >>> loc1 = Location(3,4)
        >>> print(Cancellation(11, Rider("r1", loc, loc1, 4)))
        11 -- r1: Cancel request
        """
        return "{} -- {}: Cancel request".format(self.timestamp, self.rider)


class Dropoff(Event):
    """
    Dropoff a rider
    ==========
    Attributes:
        @param Rider rider: rider who is picked up
        @param Driver driver: driver who picks up the rider
    ===========
    """

    def __init__(self, timestamp, rider, driver):
        """
        Create a pickup event

        Extended from Event

        @param int timestamp: the event's timestamp
        @param Rider rider: rider who is dropped off
        @param Driver driver: driver who drops the rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """
        Dropoff the rider

        Overrides Event.do()

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> loc = Location(0,0)
        >>> loc1 = Location(3,4)
        >>> loc2 = Location(0,4)
        >>> dp = Dropoff(12, Rider("r1", loc, loc1, 3), Driver("d1", loc2, 10))
        >>> event = dp.do(Dispatcher(), Monitor())
        >>> len(event) == 1
        True

        """
        # Notify the monitor about the event.
        # End the ride
        # driver requests a new rider

        event = []
        monitor.notify(self.timestamp, RIDER, DROPOFF, self.rider.id,
                       self.rider.destination)
        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id,
                       self.rider.destination)
        print(self)
        self.driver.end_ride()
        event.append(DriverRequest(self.timestamp, self.driver))

        return event

    def __str__(self):
        """Return a string representation of this event.

        Overrides Event.__str__()

        @type self: Dropoff
        @rtype: str

        >>> loc = Location(0,0)
        >>> loc1 = Location(3,4)
        >>> loc2 = Location(0,4)
        >>> print(Dropoff(12, Rider("r1", loc, loc1, 3), Driver("d1", loc2, 1)))
        12 -- d1: Dropoff r1
        """
        return "{} -- {}: Dropoff {}".format(self.timestamp, self.driver,
                                             self.rider)


class Pickup(Event):
    """
    Pickup a rider
    ==========
    Attributes:
        @param Rider rider: rider who is picked up
        @param Driver driver: driver who picks up the rider
    ===========
    """

    def __init__(self, timestamp, rider, driver):
        """
        Create a pickup event

        Extended from Event

        @param int timestamp: the event's timestamp
        @param Rider rider: rider who is picked up
        @param Driver driver: driver who picks up the rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """
        Pickup the rider

        Overrides Event.do()

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> d = Driver("d1", Location(0,4), 12)
        >>> r = Rider("r1", Location(0,0), Location(3,4), 3)
        >>> pk = Pickup(12, r , d )
        >>> time = d.start_drive(r.origin) # to ensure driver dest is not None
        >>> disp = Dispatcher()
        >>> mon = Monitor()
        >>> event = pk.do(disp, mon)
        >>> len(event) == 1
        True

        """
        # check if rider is there (or is waiting), if this is true,
        # then:
        # Notify the monitor about the request.
        # Start the ride
        # create dropoff event
        # rider is satisfied

        event = []

        self.driver.end_drive()
        monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id,
                           self.driver.location)

        if self.rider.status == WAITING:
            monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id,
                           self.rider.origin)

            print(self)
            time = self.driver.start_ride(self.rider)
            event.append(Dropoff(self.timestamp + time, self.rider,
                                 self.driver))  # make change if needed
            self.rider.status = SATISFIED

        else:
            event.append(DriverRequest(self.timestamp, self.driver))

        return event

    def __str__(self):
        """Return a string representation of this event.

        Overrides Event.__str__()

        @type self: Pickup
        @rtype: str

        >>> loc = Location(0,0)
        >>> loc1 = Location(3,4)
        >>> loc2 = Location(0,4)
        >>> print(Pickup(12, Rider("r1", loc, loc1, 3), Driver("d1", loc2, 10)))
        12 -- d1: Pickup r1
        """
        return "{} -- {}: Pickup {}".format(self.timestamp, self.driver,
                                            self.rider)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]

    >>> event = create_event_list("events_small.txt")
    >>> r = Rider("Dan", Location(1,1), Location(6,6), 15)
    >>> d = Driver("Arnold", Location(3,3), 2)
    >>> my_list = []
    >>> my_list.append(RiderRequest(1, r))
    >>> my_list.append(DriverRequest(10,d ))
    >>> event == my_list
    True

    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            event = None
            if event_type == "DriverRequest":
                # Create a DriverRequest event.
                driver = Driver(tokens[2], deserialize_location(tokens[3]),
                                int(tokens[4]))
                event = DriverRequest(timestamp, driver)

            elif event_type == "RiderRequest":
                # Create a RiderRequest event.
                rider = Rider(tokens[2], deserialize_location(tokens[3]),
                              deserialize_location(tokens[4]), int(tokens[5]))
                event = RiderRequest(timestamp, rider)

            if event is not None:
                events.append(event)

    return events
