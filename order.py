def compute_strating_points(streets, cars, mode="raw"):
    for car in cars:
        street_name = car.streets_taken[0]
        if mode == "raw":
            car_importance = 1
            streets[street_name].update_init_frequentation(car_importance)
        elif mode == "car_importance":
            streets[street_name].update_init_frequentation(car.importance)


def compute_starting_orders(streets, intersections):
    for inter in intersections:
    
        streets_with_importance = []
        for street_name in inter.in_streets.keys():
            street_init_frequentation = streets[street_name].init_frequentation
            streets_with_importance.append((street_name, street_init_frequentation))
        streets_with_importance.sort(key=lambda x: x[1], reverse=True)
        inter.street_order = streets_with_importance
