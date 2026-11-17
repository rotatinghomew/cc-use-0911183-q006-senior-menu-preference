def can_eat(store, resident_id, dish_id):
    resident = store.get('residents', resident_id)
    dish = store.get('dishes', dish_id)
    return not set(resident['allergens']) & set(dish['allergens']) and dish['texture'] <= resident['max_texture']


def nutrition(store, resident_id, dishes):
    resident = store.get('residents', resident_id)
    totals = {'energy': 0, 'protein': 0, 'salt': 0}
    for dish_id, portions in dishes.items():
        if portions < 0 or not can_eat(store, resident_id, dish_id):
            raise ValueError('份数或饮食适配不合法')
        dish = store.get('dishes', dish_id)
        for key in totals:
            totals[key] += dish[key] * portions
    return {'totals': totals, 'within_limits': totals['salt'] <= resident['salt_max'] and totals['energy'] >= resident['energy_min']}
