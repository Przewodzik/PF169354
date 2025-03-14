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

    def test_passengers_property(self):

        train1 = Train("Warsaw-Berlin",7)

        self.assertEqual(train1.passengers,[])



