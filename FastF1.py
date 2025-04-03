import fastf1
from fastf1.ergast import Ergast  # import current f1 data
import os
from prettytable import PrettyTable  # library to create table format

season_ = 2025
round_ = 2  # how many races have been?
sprint_round_ = 1  # how many sprints have been?
total_races = 24
total_sprints = 6

# CACHE FOLDER TO SPEED UP PROGRAM
cache_folder = 'cache folder'
if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)

fastf1.Cache.enable_cache(cache_folder)

ergast = Ergast()  # ACCESS CURRENT CHAMPIONSHIP STANDINGS DATA

print('successfully loaded data')

current_driver_standings = ergast.get_driver_standings(season=season_,
                                                       round=round_)  # GET THE CURRENT DRIVER STANDINGS DATA

# make an array of drivers' current points in order of championship position
def create_list_of_drivers_points():
    drivers_points = list()
    counter = 0

    for x in current_driver_standings.content[0]['points']:
        drivers_points.append(current_driver_standings.content[0].loc[counter]['points'])
        counter += 1

    return drivers_points

# make an array of drivers' hypothetical maximum points in order of championship position
def calculate_max_possible_season_points_remaining():
    number_of_remaining_races = total_races - round_
    number_of_remaining_sprints = total_sprints - sprint_round_

    total_points_remaining = (number_of_remaining_races * 25) + (number_of_remaining_sprints * 8)

    return total_points_remaining

# calculate the individual drivers' maximum possible points
def calculate_driver_max_points():
    driver_max_points = list()
    counter = 0

    for x in current_driver_standings.content[0]['driverId']:
        temp = current_driver_standings.content[0].loc[counter][
                   'points'] + calculate_max_possible_season_points_remaining()
        driver_max_points.append(temp)
        counter += 1

    return driver_max_points

# create an array of drivers who can still win the championship
def determine_who_can_win_championship():
    possible_champions = list()
    counter = 0
    driver_max_points = calculate_driver_max_points()

    for x in current_driver_standings.content[0]['driverId']:
        if int(driver_max_points[counter]) > int(current_driver_standings.content[0].loc[0]['points']):
            possible_champions.append(x)
            counter += 1
    return possible_champions

# print the drivers who can still win with their current points and possible maximum points
def print_possible_champions_plus_points():
    possible_champions = determine_who_can_win_championship()
    drivers_max_points = calculate_driver_max_points()
    drivers_points = create_list_of_drivers_points()
    counter = 0
    number_of_pops = len(drivers_max_points) - len(possible_champions)

    while counter < number_of_pops: # make each array the same length as number of drivers who can still win the championship
        drivers_points.pop()
        drivers_max_points.pop()
        counter += 1

    table = PrettyTable()

    table.add_column('Driver', possible_champions)
    table.add_column('current points', drivers_points)
    table.add_column('max points', drivers_max_points)
    print(table)


print_possible_champions_plus_points()