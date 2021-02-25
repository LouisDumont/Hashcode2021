def get_car_importance(car, streets, total_time, car_base_score):
	min_travel_duration = 0
	## TODO: add estimated waiting time at intersection for importance
	for street in car.streets_taken[1:]:
		min_travel_duration += streets[street].travel_time

	if total_time - min_travel_duration >= 0:
		return max(0, car_base_score + total_time - min_travel_duration)
	return 0

def update_cars_importance(cars, streets, total_time, car_base_score):
	for car in cars:
		car.update_importance(get_car_importance(car, streets, total_time, car_base_score))
