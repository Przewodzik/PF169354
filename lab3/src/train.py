class Train:
    def __init__(self, route: str, carriages: int,fare_per_carriage: int | float = 100):
        self.route = route
        self.carriages = carriages
        self._passengers = []
        self.__fare_per_carriage = fare_per_carriage

    def calculate_fare(self):
        return self.carriages * self.__fare_per_carriage

    def add_passenger(self, passenger: str):
        if isinstance(passenger, str):
            if passenger.strip() == '':
                raise ValueError("Passenger name cannot be empty")
            self._passengers.append(passenger)
        else:
            raise TypeError("Passenger name must be a string")

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, route: str):
        if isinstance(route, str):
            if route.strip() == "":
                raise ValueError("Route cannot be empty")
            self._route = route
        else:
            raise TypeError("Route must be a string")

    @property
    def carriages(self):
        return self._carriages

    @carriages.setter
    def carriages(self, carriages: int):
        if isinstance(carriages, int):
            if carriages <= 0:
                raise ValueError("Carriages must be greater than 0")
            self._carriages = carriages
        else:
            raise TypeError("Carriages must be an integer")

    @property
    def passengers(self):
        return self._passengers.copy()

    @property
    def fare_per_carriage(self):
        return self.__fare_per_carriage

    @fare_per_carriage.setter
    def fare_per_carriage(self, fare_per_carriage: int | float):
        if isinstance(fare_per_carriage,(int,float)):
            if fare_per_carriage <= 0:
                raise ValueError("Fare per carriage must be greater than 0")
            self.__fare_per_carriage = fare_per_carriage
        else:
            raise TypeError("Fare per carriage must be a number")


