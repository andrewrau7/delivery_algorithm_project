# Andrew Rau
# ID: 010266752
import csv
from HashingTable import HashingTable
from Truck import *
from datetime import datetime

# Establish an interface for the user to interact with
user_query_package_string = input("Enter a package ID to view info for desired package. (Enter '0' to view all): ")

# Exception handlers included to prevent errors due to input.
try:
    user_query_package_id = int(user_query_package_string)
except:
    print("Integer required")
    exit()

if not(user_query_package_id in range(0, 41)):
    print("Package ID doesn't exist")
    exit()


# Establish an interface for the user to interact with
user_query_time_string = input(
    "Enter a time between 8am-5pm (00:00 AM/PM format) to view all package information at that time: ")
user_query_datetime_string = "01/01/2023 " + user_query_time_string

# Exception handlers included to prevent errors due to input.
try:
    user_query_datetime = datetime.strptime(user_query_datetime_string, "%m/%d/%Y %I:%M %p")
except:
    print("Invalid time format")
    exit()

if user_query_datetime < datetime(year=2023, month=1, day=1, hour=8) or user_query_datetime > datetime(year=2023,
                                                                                                       month=1, day=1,
                                                                                                       hour=17):
    print("Invalid time chosen")
    exit()

"""
user_query_datetime object is used as parameter throughout program in order to stop any methods that directly affect
packages and trucks in order to reflect and accurate status of those objects at the specified time.
"""

# Initialize a hash table object to hold package data
package_inventory = HashingTable(40)

# Initialize a set to hold different package deadlines
different_deadlines_set = set()
# Open the packages.csv file to be parsed.
with open('packages.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    delayed_package_id_list = [6, 25, 28, 32]
    for row in csv_reader:
        address = row[2] + ", " + row[3]  # combine rows to form a full address.
        different_deadlines_set.add(row[5])  # if new deadline is found, add to the set.
        if int(row[0]) not in delayed_package_id_list:
            package_inventory.insert(int(row[0]), row[1], address, row[4], row[5], row[6], "In hub @ 8:00AM")
        else:
            package_inventory.insert(int(row[0]), row[1], address, row[4], row[5], row[6], "Delayed until 9:05 AM")

Truck.delivery_deadline_list = sorted(different_deadlines_set, reverse=True)  # sort the set for index purposes
Truck.delivery_deadline_list.remove('EOD')
Truck.delivery_deadline_list.append('EOD')  # ensure EOD packages are last in the index

# Open the distances.csv file to be parsed.
with open('distances.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:      # first row in the distances.csv file contains addresses that
            for address in row:  # are stored in the LocationHandler file
                LocationHandler.address_list.append(address)
            line_count += 1
            continue
        if line_count > 0:  # distance_matrix in LocationHandler file is filled row by row from csv file
            LocationHandler.distance_matrix.append([])
            for distance in row:
                LocationHandler.distance_matrix[line_count - 1].append(distance)
            line_count += 1

LocationHandler.fillDistanceMatrix()  # Distance_matrix is populated on both sides to ensure
                                      # order of inserted indexes does not matter.
                                      # O(a^2)

first_truck = Truck(1)
second_truck = Truck(2)
third_truck = Truck(3)

# Create list of package id's for manual loading.
truck_1_package_id_list = [1, 4, 13, 14, 15, 16, 17, 19, 20, 21, 27, 33, 34, 35, 39, 40]
truck_2_package_id_list = [3, 6, 7, 11, 18, 23, 24, 25, 26, 29, 30, 31, 32, 36, 37, 38]
truck_3_package_id_list = [2, 5, 8, 9, 10, 12, 22, 28]

# Truck_2 is chosen to carry all delayed packages. currTime is changed to reflect the delay.
second_truck.currTime = datetime(year=2023, month=1, day=1, hour=9, minute=5)

# Manual loading iterations.
# Worst case is O(p²) where p is the total number of packages to be delivered.
for package_id in truck_1_package_id_list:
    first_truck.loadPackage(package_inventory.get_package(package_id), user_query_datetime)

for package_id in truck_2_package_id_list:
    second_truck.loadPackage(package_inventory.get_package(package_id), user_query_datetime)

for package_id in truck_3_package_id_list:
    third_truck.loadPackage(package_inventory.get_package(package_id), user_query_datetime)


# Optimize package loads within trucks to ensure mileage efficiency.
first_truck.optimizePackages()  # O(d²p²)
second_truck.optimizePackages()

# Method call to deliver truck packages algorithmically
first_truck.deliverTruckPackages(user_query_datetime)  # O(ap²)
second_truck.deliverTruckPackages(user_query_datetime)

# Returns a driver to the hub so truck_3 can be driven
first_truck.returnToHub(user_query_datetime)

# Truck_3 is carrying package 9 that has a change of address at 10:20 AM
third_truck.currTime = datetime(year=2023, month=1, day=1, hour=10, minute=20)
if user_query_datetime > third_truck.currTime:
    package_inventory.get_package(9).delivery_address = "410 S State St."

# Deliver last packages on truck_3
third_truck.deliverTruckPackages(user_query_datetime)

test_miles = first_truck.total_mileage + second_truck.total_mileage + third_truck.total_mileage
print()
print("Total Miles Traveled: " + str(test_miles) + "\n")

# Display package data with respect to the user's chosen package and time.
if user_query_package_id == 0:
    for i in range(1, 41):
        package_inventory.lookup(i, user_query_datetime)  # Worst case of O(p²) where p is the total number of packages
else:
    package_inventory.lookup(user_query_package_id, user_query_datetime)

"""
Total Space-time complexity for the program is O(ap² + d²p² + a² + p²) 
Where a is the number of addresses
      p is the total number of packages
      d is the number of deadlines
"""