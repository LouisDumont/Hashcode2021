def get_car_importance(car, streets, total_time, car_base_score):
	min_travel_duration = 0
	## TODO: add estimated waiting time at intersection for importance
	for street in car.streets_taken:
		min_travel_duration += streets[street].travel_time

	return max(0, car_base_score + total_time - min_travel_duration)

def update_cars_importance(cars, streets, total_time, car_base_score):
	for car in cars:
		car.update_importance(get_car_importance(car, streets, total_time, car_base_score))