import datetime

import LocationHandler


class Truck:
    delivery_deadline_list = []

    # Constructor for Truck objects. Location is set to WGU hub. Time is set to start of day at 8am.
    # Package_table is transformed into a matrix according to different delivery_deadline_list entries. Each list
    # within the package_table represents a list of packages that have the same delivery deadline.
    def __init__(self, truck_num):
        self.package_table = []
        self.currTime = datetime.datetime(year=2023, month=1, day=1, hour=8)
        self.total_mileage = 0
        self.truck_number = truck_num
        self.current_location = "4001 South 700 East"
        for i in range(len(Truck.delivery_deadline_list)):
            self.package_table.append([])

    # Method for loading packages onto a specific truck. Delivery status is updated along with the specified package's
    # truck reference.
    # Bucket is determined by index of the package's delivery deadline within the Truck class's
    # delivery_deadline_list.
    # Space-time complexity is O(d) where d is the number of deadlines.
    def loadPackage(self, package, user_query_time):
        if user_query_time < self.currTime:
            return
        else:
            package.delivery_status = "On Truck " + str(self.truck_number) + " @ " + self.currTime.time().strftime(
                "%I:%M %p")
            bucket = Truck.delivery_deadline_list.index(package.delivery_deadline)
            package.index_number = bucket
            package.truck = self
            self.package_table[bucket].append(package)

    # Method for delivering a package from a truck. Package delivery status is updated along with being removed
    # from the truck's table of packages.
    def unloadPackage(self, package):
        package.delivery_status = "Delivered @ " + self.currTime.strftime("%I:%M %p") + \
                                  " by Truck " + str(package.truck.truck_number)
        bucket = package.index_number
        package.truck = ""
        self.package_table[bucket].remove(package)

    # Method for optimizing table of packages for a truck.
    # Searches each list of packages in a truck's package table and adds packages to an earlier deadline list if they
    # are within a marginal distance (2 miles) of a package with an earlier deadline.
    # Space-time complexity is O((d^2)(p^2)) where is the number of deadlines and p is the total amount of packages
    # contained within a given truck.
    def optimizePackages(self):
        i = 0
        while i < len(self.package_table) - 1:
            for earlier_package in self.package_table[i]:
                k = i + 1
                while k < len(self.package_table):
                    for later_package in self.package_table[k]:
                        if LocationHandler.distanceBetweenAddresses(earlier_package.delivery_address,
                                                                    later_package.delivery_address) < 2:
                            self.package_table[i].append(later_package)
                            later_package.index_number = i
                            self.package_table[k].remove(later_package)
                    k += 1
            i += 1

    # Method for delivering a given truck's packages. Utilizing the Nearest Neighbor algorithm, the next package to
    # be delivered within the given package list is found with the getClosestPackage method.
    # Distance is then calculated from the truck's address, then added to the truck's mileage, then used to find the
    # time needed to deliver the package. The time is then added to the truck's currTime variable, the truck's
    # location is updated, and the package is then officially unloaded.
    # Space-time complexity is O(a(p^2)) where a is the number of addresses in the address_list and
    # p is the number of packages in the given truck's package table.
    def deliverTruckPackages(self, user_query_time):
        for package_list in self.package_table:  # O(p)
            while len(package_list) > 0:
                next_package = LocationHandler.getClosestPackage(self.current_location, package_list)  # O(p * a)
                traveled_miles = LocationHandler.distanceBetweenAddresses(self.current_location,
                                                                          next_package.delivery_address)  # O(a)
                self.currTime += datetime.timedelta(hours=traveled_miles / 18)
                if self.currTime > user_query_time:
                    return
                self.total_mileage += traveled_miles
                self.current_location = next_package.delivery_address
                self.unloadPackage(next_package)

    # Method for returning a truck, and thus a driver, to the hub. The truck's mileage and currTime variable are
    # updated to reflect the travel back.
    def returnToHub(self, user_query_time):
        if self.currTime > user_query_time:
            return
        else:
            driver_return_miles = LocationHandler.distanceBetweenAddresses("4001 South 700 East", self.current_location)
            self.total_mileage += driver_return_miles
            self.currTime += datetime.timedelta(hours=driver_return_miles / 18)
