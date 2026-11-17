from math import ceil


def quote_menu(store, portions):
    ingredients = {}
    batches = {}
    for dish_id, count in portions.items():
        if not isinstance(count, int) or count < 0:
            raise ValueError('厨房份数须为非负整数')
        dish = store.get('dishes', dish_id)
        batch_count = ceil(count / dish['batch_size'])
        batches[dish_id] = batch_count
        for ingredient, grams in dish['ingredients_per_batch'].items():
            ingredients[ingredient] = ingredients.get(ingredient, 0) + grams * batch_count
    cents = 0
    for ingredient, grams in ingredients.items():
        item = store.get('ingredients', ingredient)
        cents += ceil(grams * item['cents_per_kg'] / 1000)
    return {'batches': batches, 'ingredients_grams': ingredients, 'cents': cents}
