
class Train:

    def __init__(self, route:str, carriages:int):

        self.route = route
        self.carriages = carriages


    def calculate_fare(self):

        return self.carriages * 100


    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, route:str):

        if isinstance(route,str):

            if route == "":
                raise ValueError("route cannot be empty")
            self._route = route

        else:
            raise TypeError("route must be a string")


    @property
    def carriages(self):
        return self._carriages

    @carriages.setter
    def carriages(self, carriages:int):

        if isinstance(carriages,int):
            if carriages <= 0:
                raise ValueError("carriages must be greater than 0")
            self._carriages = carriages

        else:
            raise TypeError("carriages must be an integer")







