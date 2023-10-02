from typing import List, Any
from Package import *


class HashingTable:

    # Constructor for initializing PackageHashingTable objects. Can be initialized with variable amount of buckets.
    def __init__(self, input_size=10):
        self.hash_table = []
        for i in range(input_size):
            self.hash_table.append([])

    # Method for adding Package objects to the hash table. Bucket is determined by taking the remainder of a
    # package id number divided by the total amount of buckets.
    # Space-time complexity of O(1) for inserts.
    def insert(self, id_num, deliv_add, deliv_dead, deliv_city, deliv_zip, pack_weight, deliv_status):
        bucket = id_num % len(self.hash_table)
        new_package = Package(id_num, deliv_add, deliv_dead, deliv_city, deliv_zip, pack_weight, deliv_status)
        self.hash_table[bucket].append(new_package)

    # Look-up function for finding a specific package by id number.
    # Returns a string containing specific package information depending on delivery status at a specific input time.
    # Space-time complexity of O(p) where p is the number of packages in the hash table.
    # Average case would be O(1) if packages were evenly distributed among hash table buckets.
    def lookup(self, id_num, user_query_time):
        bucket = id_num % len(self.hash_table)
        for package in self.hash_table[bucket]:
            if package.id == id_num and "On Truck" in package.delivery_status:
                print("Package ID: " + str(package.id) + "\n" +
                      "Package Address: " + package.delivery_address + ", " + package.delivery_city + " " + package.delivery_zip_code + "\n"
                      "Package Deadline: " + package.delivery_deadline + "\n" +
                      "Package Weight: " + package.package_weight + "kg" + "\n" +
                      "Package Delivery Status: On Truck " + str(package.truck.truck_number) + " @ " + user_query_time.strftime("%I:%M %p") + "\n")
            elif package.id == id_num and "In hub" in package.delivery_status:
                print("Package ID: " + str(package.id) + "\n" +
                      "Package Address: " + package.delivery_address + ", " + package.delivery_city + " " + package.delivery_zip_code + "\n"
                      "Package Deadline: " + package.delivery_deadline + "\n" +
                      "Package Weight: " + package.package_weight + "kg" + "\n" +
                      "Package Delivery Status: In hub @ " + user_query_time.strftime("%H:%M %p") + "\n")
            elif package.id == id_num:
                print("Package ID: " + str(package.id) + "\n" +
                      "Package Address: " + package.delivery_address + ", " + package.delivery_city + " " + package.delivery_zip_code + "\n"
                      "Package Deadline: " + package.delivery_deadline + "\n" +
                      "Package Weight: " + package.package_weight + "kg" + "\n" +
                      "Package Delivery Status: " + package.delivery_status + "\n")

    # Method for returning a package object by id number.
    # Space-time complexity of O(p) where p is the number of packages in the hash table.
    # Average case would be O(1) if packages were evenly distributed among hash table buckets.
    def get_package(self, package_id):
        bucket = package_id % len(self.hash_table)
        for package in self.hash_table[bucket]:
            if package.id == package_id:
                return package
