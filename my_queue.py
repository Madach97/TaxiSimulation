class Queue:
    """
    implement a queue

    """
    def __init__(self):
        """
        Create a queue

        @rtype: None

        """
        self._items = []

    def add(self, item):
        """
        add items to queue

        @param obj item: the object to add to the queue
        @rtype: None

        """
        self._items.append(item)

    def remove(self, item):
        """
        removes the item from the queue

        @param obj item: the item to be removed
        @rtype: None

        """
        self._items.remove(item)

    def pop_(self):
        """
        removes and returns the first item in the list

        @rtype: obj

        """
        self._items.pop()

    def __str__(self):
        """
        String representation of the items in queue
        @rtype: str

        """
        s = ""
        for i in self._items:
            s += i + "\n"

        return s

    def __eq__(self, other):
        """
        Compares this queue with another object

        @param Any other: object to compare self to
        @rtype: bool

        """
        return type(self) == type(other) and self._items == other._items

    def is_empty(self):
        """
        Check if the queue is empty

        @rtype: bool

        """
        return len(self._items) == 0




