import unittest
from meals.app import Application
from meals.store import Store
from meals.nutrition import can_eat, nutrition
from meals.evidence import meal_totals, save_meal
from meals.kitchen import quote_menu


class MealTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(':memory:')
        Application(self.store).seed()

    def tearDown(self):
        self.store.close()

    def test_allergen(self):
        self.assertFalse(can_eat(self.store, 'r1', 'pudding'))

    def test_texture(self):
        self.assertFalse(can_eat(self.store, 'r1', 'fish'))

    def test_valid_nutrition(self):
        self.assertTrue(nutrition(self.store, 'r1', {'soft_rice': 1})['within_limits'])

    def test_incompatible_nutrition_rejected(self):
        with self.assertRaises(ValueError):
            nutrition(self.store, 'r1', {'fish': 1})

    def test_batch_rounding(self):
        self.assertEqual(quote_menu(self.store, {'soft_rice': 11})['batches'], {'soft_rice': 2})

    def test_shared_ingredient(self):
        value = quote_menu(self.store, {'soft_rice': 1, 'fish': 1})
        self.assertEqual(value['ingredients_grams']['rice'], 1300)

    def test_negative_portions(self):
        with self.assertRaises(ValueError):
            quote_menu(self.store, {'soft_rice': -1})

    def test_missing_waste_is_preserved(self):
        self.assertEqual(meal_totals(self.store)['fish']['missing_leftover'], 1)

    def test_invalid_leftover(self):
        row = dict(self.store.get('meals', 'm1'), leftover_grams=300)
        with self.assertRaises(ValueError):
            save_meal(self.store, row)

    def test_empty_menu_cost(self):
        self.assertEqual(quote_menu(self.store, {})['cents'], 0)
