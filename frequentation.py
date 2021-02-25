def compute_frequentation(streets, cars, mode="raw"):
    for car in cars:
        for street_name in car.streets_taken:
            if mode == "raw":
                car_importance = 1
            streets[street_name].update_importance(car_importance)
