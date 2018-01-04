from driver import Driver
from rider import *
from location import Location


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """
    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        self._drivers = []
        self._riders = []

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str

        >>> disp = Dispatcher()
        >>> print(disp)
        Riders:
        Drivers:
        <BLANKLINE>
        >>> r = Rider("n1", Location(0,0), Location(3,4), 2)
        >>> driver = disp.request_driver(r)
        >>> print(disp)
        Riders:
         r
        Drivers:
        <BLANKLINE>
        >>> d = Driver( "d2", Location(0,3), 10)
        >>> rider = disp.request_rider(d)
        >>> print(disp)
        Riders:
        Drivers:
         d2
        <BLANKLINE>
        """
        s = "Riders: \n"
        for r in self._riders:
            s += " " + str(r) + "\n"

        s += "Drivers: \n"
        for d in self._drivers:
            s += " " + str(d) + "\n"

        return s

    def request_driver(self, rider):
        """
        Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None

        >>> disp = Dispatcher()
        >>> d = Driver ( "d", Location(5,5), 10)
        >>> d1 = Driver ( "d1", Location(31,29), 20)
        >>> d2 = Driver ( "d2", Location(0,3), 5)
        >>> disp.request_rider(d)
        >>> disp.request_rider(d1)
        >>> disp.request_rider(d2)
        >>> d.is_idle = False
        >>> r = Rider("n1", Location(0,0), Location(3,4), 2)
        >>> driver = disp.request_driver(r)
        >>> print(driver)
        d2
        """
        driver = None

        if len(self._drivers) == 0:
            self._riders.append(rider)

        else:
            min_time = -1   # just to have a starting value for min
            for d in self._drivers:
                if d.is_idle:
                    if min_time == -1:  # means that d is the 1st idle driver
                        # d's time is set as the minimum
                        min_time = d.get_travel_time(rider.origin)
                        driver = d

                    elif min_time > d.get_travel_time(rider.origin):
                        # if time of this driver is less than the min time so
                        # far then this driver's time is min.
                        min_time = d.get_travel_time(rider.origin)
                        driver = d
        #print(driver)
        return driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None

        >>> disp = Dispatcher()
        >>> r = Rider("r", Location(0,0), Location(3,4), 2)
        >>> r1 = Rider("r1", Location(5,20), Location(5,6), 5)
        >>> r2 = Rider("r2", Location(4,0), Location(13,14), 10)
        >>> disp.request_driver(r)
        >>> disp.request_driver(r1)
        >>> disp.request_driver(r2)
        >>> d = Driver ( "d", Location(5,5), 10)
        >>> d1 = Driver ( "d1", Location(31,29), 20)
        >>> d2 = Driver ( "d2", Location(0,3), 5)
        >>> rider = disp.request_rider(d)
        >>> print(rider)
        r
        >>> rider = disp.request_rider(d1)
        >>> print(rider)
        r1
        >>> rider = disp.request_rider(d2)
        >>> print(rider)
        r2

        """
        rider = None
        if driver not in self._drivers:
            self._drivers.append(driver)

        if not len(self._riders) == 0:
            rider = self._riders.pop(0)

        return rider

    def cancel_ride(self, rider):
        """
        Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None

        >>> disp = Dispatcher()
        >>> r1 = Rider("r1", Location(5,20), Location(5,6), 5)
        >>> driver = disp.request_driver(r1)
        >>> r1 in disp._riders
        True
        >>> disp.cancel_ride(r1)
        >>> r1 in disp._riders
        False
        """
        if rider in self._riders:
            self._riders.remove(rider)
