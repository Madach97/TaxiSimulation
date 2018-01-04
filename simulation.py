from container import PriorityQueue
from dispatcher import Dispatcher
from event import Event, create_event_list
from event import *
from monitor import Monitor


class Simulation:
    """A simulation.

    This is the class which is responsible for setting up and running a
    simulation.

    The API is given to you: your main task is to implement the run
    method below according to its docstring.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _dispatcher: Dispatcher
    #     The dispatcher associated with the simulation.

    def __init__(self):
        """Initialize a Simulation.

        @type self: Simulation
        @rtype: None
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """Run the simulation on the list of events in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: Simulation
        @type initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]

        >>> events = []
        >>> loc = Location(0,0)
        >>> events.append(RiderRequest(2,Rider("r1", loc, Location(3,4), 4)))
        >>> events.append(DriverRequest(3, Driver("d1", Location(0,4), 10)))
        >>> sim = Simulation()
        >>> sim.run(events)
        {'rider_wait_time': 1.0, 'driver_ride_distance': 7.0, 'driver_total_distance': 11.0}

        # Above line couldn't be changed to go to next line because doing that
        # made the doctest compare the output so that it also flows to the next
        # line

        """
        # Add all initial events to the event queue.
        # Until there are no more events, remove an event
        # from the event queue and do it. Add any returned
        # events to the event queue.

        for event in initial_events:
            self._events.add(event)

        new_events = []
        while not self._events.is_empty():
            new_events = self._events.remove().do(self._dispatcher,
                                                  self._monitor)
            if new_events is not None:
                for event in new_events:
                    self._events.add(event)


        return self._monitor.report()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    events = create_event_list("events.txt")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)
