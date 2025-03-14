import unittest
from lab3.src.ship import Ship


class TestShipInitialization(unittest.TestCase):

    def setUp(self):
        pass

    def testCreation(self):
        ship1 = Ship("Rotterdam",7)
        self.assertIsInstance(ship1, Ship)


    def test_initialization(self):
        ship1 = Ship("Rotterdam", 7)
        self.assertEqual(ship1.destination, "Rotterdam")
        self.assertEqual(ship1.voyage_duration, 7)

    def test_calculate_fuel(self):
        ship1 = Ship("Rotterdam", 7)
        ship2 = Ship("Singapore", 5)
        ship3 = Ship("Gdańsk",0)

        self.assertEqual(ship1.calculate_fuel(),700)
        self.assertEqual(ship2.calculate_fuel(),500)
        self.assertEqual(ship3.calculate_fuel(),0)

    def test_add_crew_member(self):
        ship1 = Ship("Rotterdam", 7)

        ship1.add_crew_member("Captain Smith")
        self.assertIn("Captain Smith", ship1.crew)

        ship1.add_crew_member("First Mate Jones")
        self.assertIn("First Mate Jones",ship1.crew)

        ship1.add_crew_member("Engineer Roberts")
        self.assertIn("Engineer Roberts",ship1.crew)

        ship1.add_crew_member("Captain Smith")
        ship1.add_crew_member("Captain Smith")

        self.assertEqual(ship1.crew.count("Captain Smith"), 3)

        with self.assertRaises(ValueError):
            ship1.add_crew_member("")



    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()