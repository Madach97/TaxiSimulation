from location import manhattan_distance, Location
"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
@type RIDER: str
    A constant used for the Rider activity category.
@type DRIVER: str
    A constant used for the Driver activity category.
@type REQUEST: str
    A constant used for the request activity description.
@type CANCEL: str
    A constant used for the cancel activity description.
@type PICKUP: str
    A constant used for the pickup activity description.
@type DROPOFF: str
    A constant used for the dropoff activity description.
"""

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @type timestamp: int
        The time at which the activity occurred.
    @type description: str
        A description of the activity.
    @type identifier: str
        An identifier for the person doing the activity.
    @type location: Location
        The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity.

        @type self: Activity
        @type timestamp: int
        @type description: str
        @type identifier: str
        @type location: Location
        @rtype: None
        """
        self.description = description
        self.time = timestamp
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    # @type _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor.

        @type self: Monitor
        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @type self: Monitor
        @rtype: str
        """
        return "Monitor ({} drivers, {} riders)".format(
                len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitor of the activity.

        @type self: Monitor
        @type timestamp: int
            The time of the activity.
        @type category: DRIVER | RIDER
            The category for the activity.
        @type description: REQUEST | CANCEL | PICKUP | DROP_OFF
            A description of the activity.
        @type identifier: str
            The identifier for the actor.
        @type location: Location
            The location of the activity.
        @rtype: None
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self):
        """Return a report of the activities that have occurred.

        @type self: Monitor
        @rtype: dict[str, object]
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @type self: Monitor
        @rtype: float

        """
        wait_time = 0
        count = 0
        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        return wait_time / count

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        @type self: Monitor
        @rtype: float

        # this method is checked when simulation is tested
        # it is too complicated to write doctest separately as it will involve
        # creating a new list of events, putting them in the activities
        # dictionary and then checking avg total distance

        # >>> loc = Location(0,0)
        # >>> events = []
        # >>> events.append(RiderRequest(2,Rider("r1", loc, Location(3,4), 4)))
        # >>> events.append(DriverRequest(3, Driver("d1", Location(0,4), 10)))
        # >>> sim = Simulation()
        # >>> sim.run(events)
        # >>> my_list = []
        # >>> my_list.append(RiderRequest(1, r))
        # >>> my_list.append(DriverRequest(10,d ))
        # >>> my_list.append(Pickup(12, r, d))
        # >>> my_list.append(Cancellation(16, r))
        # >>> my_list.append(Dropoff(10 + d.start_ride(r), r, d))
        # >>> my_list.append(DriverRequest(17, r))
        # >>> for x in my_list :
        # >>>    x.do()

        """
        distance = 0
        for activities in self._activities[DRIVER].values():
            # if the ith event is a request, that is when the driver starts a
            # ride the i+1th event must be a pickup, which will tell us when the
            # ride ended and where the drive started. i+2th event must be a
            # dropoff which will tell us where the ride ended

            for i in range(len(activities) - 2):

                if activities[i].description == REQUEST:
                    start_drive = activities[i].location
                    end_drive = activities[i + 1].location
                    distance += manhattan_distance(start_drive, end_drive)

                    # check if the dropoff actually did happen or if the
                    # rider cancelled the ride before pickup
                    if activities[i + 2].description == DROPOFF:
                        start_ride = end_drive
                        end_ride = activities[i + 2].location
                        distance += manhattan_distance(start_ride, end_ride)


        return float((distance) / len(self._activities[DRIVER]))

    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.
        @type self: Monitor
        @rtype: float

        # this method is checked when simulation is tested
        # it is too complicated to write doctest separately as it will involve
        # creating a new list of events, putting them in the activities
        # dictionary and then checking avg total distance

        """
        distance = 0
        for activities in self._activities[DRIVER].values():
            # if the ith event is a pickup where the drive started.
            # i+1th event may or may not be a dropoff. if it is a dropoff, it
            # will tell us where the ride ended

            for i in range(len(activities) - 1):
                # check if the dropoff actually did happen or if the
                # rider cancelled the ride before pickup
                if (activities[i].description == PICKUP and
                    activities[i + 1].description == DROPOFF):
                    start_ride = activities[i].location
                    end_ride = activities[i + 1].location
                    distance += manhattan_distance(start_ride, end_ride)

        return float(distance / len(self._activities[DRIVER]))
