def compute_streets_frequentation(streets, cars, mode="raw"):
    for car in cars:
        for street_name in car.streets_taken:
            street_name = street_name
            if mode == "raw":
            	car_importance = 1
            	streets[street_name].update_frequentation(car_importance)
            elif mode=="car_importance":
            	streets[street_name].update_frequentation(car.importance)


def compute_inters_importance(streets, intersections):
    for inter in intersections:
        # Get frequantation
        sum_frequentation = 0
        for street_name in inter.in_streets.keys():
            street_frequentation = streets[street_name].frequentation
            inter.update_street_importance(street_name, street_frequentation)
            sum_frequentation += street_frequentation
        # Get importances from frequentations
        for street_name in inter.in_streets.keys():
            street_importance = inter.in_streets[street_name] / sum_frequentation
            inter.update_street_importance(street_name, street_importance)

