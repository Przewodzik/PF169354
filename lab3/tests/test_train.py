import unittest
from lab3.src.train import Train

class TestTrainInitialization(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creation(self):
        train = Train("Warsaw-Berlin",7)
        self.assertIsInstance(train,Train)

    def test_initialization(self):
        train = Train("Warsaw-Berlin",7)
        self.assertEqual(train.route, "Warsaw-Berlin")
        self.assertEqual(train.carriages,7)

        with self.assertRaises(ValueError):
            Train("",7)

        with self.assertRaises(TypeError):
            Train(121,7)

        with self.assertRaises(ValueError):
            Train("Warsaw-Berlin",0)

        with self.assertRaises(ValueError):
            Train("Warsaw-Berlin",-5)

        with self.assertRaises(TypeError):
            Train("Warsaw-Berlin","7")

    def test_calculate_fare(self):

        train1 = Train("Warsaw-Berlin",7)
        train2 = Train("Warsaw-Prague",5)

        self.assertEqual(train1.calculate_fare(),700)
        self.assertEqual(train2.calculate_fare(),500)

        train1.fare_per_carriage = 200

        self.assertEqual(train1.calculate_fare(),1400)

    def test_passengers_property(self):

        train1 = Train("Warsaw-Berlin",7)

        self.assertEqual(train1.passengers,[])

        original_length = len(train1.passengers)
        passengers = train1.passengers

        passengers.append('Alice')

        self.assertNotIn('Alice',train1.passengers)
        self.assertEqual(len(train1.passengers), original_length)


    def test_add_passenger(self):
        train1 = Train("Warsaw-Berlin",7)

        train1.add_passenger('John')

        self.assertIn('John',train1.passengers)

        train1.add_passenger('Alice')

        self.assertIn('Alice',train1.passengers)

        train1.add_passenger('Bob')

        self.assertIn('Bob',train1.passengers)

        train1.add_passenger('Bob')
        train1.add_passenger('Bob')

        self.assertEqual(train1.passengers.count('Bob'),3)


        with self.assertRaises(ValueError):
            train1.add_passenger("")

        with self.assertRaises(TypeError):
            train1.add_passenger(7)

    def test_fare_per_carriage_property(self):
        train1 = Train("Warsaw-Berlin",7)

        self.assertEqual(train1.fare_per_carriage,100)

        train1.fare_per_carriage = 150

        self.assertEqual(train1.fare_per_carriage,150)

        with self.assertRaises(ValueError):
            train1.fare_per_carriage = 0

        with self.assertRaises(ValueError):
            train1.fare_per_carriage = -50

        with self.assertRaises(TypeError):
            train1.fare_per_carriage = "expensive"






