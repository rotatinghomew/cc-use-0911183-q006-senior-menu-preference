def save_meal(store, row):
    store.get('residents', row['resident'])
    store.get('dishes', row['dish'])
    if row['delivered_grams'] < 0 or row['leftover_grams'] is not None and not 0 <= row['leftover_grams'] <= row['delivered_grams']:
        raise ValueError('送达或剩餐重量不合法')
    return store.put('meals', row)


def meal_totals(store):
    values = {}
    for row in store.all('meals'):
        dish = values.setdefault(row['dish'], {'orders': 0, 'delivered_grams': 0, 'known_leftover_grams': 0, 'missing_leftover': 0})
        dish['orders'] += 1
        dish['delivered_grams'] += row['delivered_grams']
        if row['leftover_grams'] is None:
            dish['missing_leftover'] += 1
        else:
            dish['known_leftover_grams'] += row['leftover_grams']
    return values
