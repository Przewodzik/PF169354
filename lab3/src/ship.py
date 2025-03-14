
class Ship:

    def __init__(self,destination: str, voyage_duration: int):

        if isinstance(destination,str):
            self.destination = destination
        else:
            raise TypeError("Destination must be a string")

        if isinstance(voyage_duration,int):
            self.voyage_duration = voyage_duration
        else:
            raise TypeError("Voyage duration must be a integer")

        self.crew = []

    def calculate_fuel(self):
        if self.voyage_duration >= 0:
            return self.voyage_duration * 100
        raise ValueError("Voyage duration must be a positive integer")

    def add_crew_member(self,crew_member:str):

        if isinstance(crew_member,str):
            if crew_member == "":
                raise ValueError("Crew member cannot be empty")
            self.crew.append(crew_member)

        else:
            raise TypeError("Crew member must be a string")
