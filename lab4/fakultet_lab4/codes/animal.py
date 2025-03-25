class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._mood = "happy"

    def speak(self):
        return "Sound"

    def description(self):
        return f"{self.name} is {self.age} years old and is {self._mood}."

    def update_mood(self, new_mood):
        self._mood = new_mood


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def speak(self):
        return "Bark"

    def fetch(self, item):
        return f"{self.name} fetches the {item}."

    def play(self, toy):
        return f"{self.name} plays with {toy}."

    @staticmethod
    def run():
        return "Dog is running."

    @classmethod
    def create_default(cls):
        return cls("Buddy", 3, "Mixed")


def main():
    dog1 = Dog("Max", 5, "Labrador")
    dog2 = Dog("Charlie", 3, "Beagle")
    print(dog1.description())
    print(dog1.speak())
    print(dog1.fetch("stick"))
    print(Dog.run())
    print(dog2.description())
    print(dog2.speak())
    dog2.update_mood("excited")
    print(dog2.description())
    default_dog = Dog.create_default()
    print(default_dog.description())
    print(default_dog.speak())
    play_result = dog1.play("frisbee")
    print(play_result)
    x = dog1.fetch("ball")
    print(x)
    result = dog2.run()
    print(result)
    status = "done" if x else "not done"
    print("Fetch status:", status)
    print("Exercise completed.")


if __name__ == "__main__":
    main()
