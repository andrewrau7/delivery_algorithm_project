# list for storing different addresses
address_list = []
# list for storing distances between addresses. Becomes a 2d matrix as the distances.csv file is read.
distance_matrix = []


# Method for populating entire matrix with values. Utilized to ensure order of input index values does not matter.
# Space-time complexity of O(a^2) where a is the number of addresses in the address_list.
def fillDistanceMatrix():
    row_index = 0
    for row in distance_matrix:
        column_index = 0
        for distance_value in row:
            distance_matrix[row_index][column_index] = distance_matrix[column_index][row_index]
            column_index += 1
        row_index += 1


# finds distance between two input addresses.
# iterates through entire address list to find index of addresses.
# indexes are then passed as arguments to the distance_matrix to find and return distance value.
# space-time complexity is O(a) where a is the number of addresses in the address_list.
def distanceBetweenAddresses(address_1, address_2):
    global address_2_index, address_1_index
    for full_address in address_list:
        if address_1 in full_address:
            address_1_index = address_list.index(full_address)
        if address_2 in full_address:
            address_2_index = address_list.index(full_address)

    return float(distance_matrix[address_1_index][address_2_index])


# Method for finding a package delivery address that is closest to a truck's current address.
# A list of packages is iterated through to determine the closest package utilizing
# the distanceBetweenAddresses method and a min_distance variable that is reset if a shorter distance is found.
# Space-time complexity is O(a * p) where a is the number of addresses in the address list and p is the number
# of packages in the package list that is passed as an argument.
def getClosestPackage(fromAddress, truckPackages):
    min_distance = 100
    for package in truckPackages:
        if distanceBetweenAddresses(fromAddress, package.delivery_address) < min_distance:
            min_distance = distanceBetweenAddresses(fromAddress, package.delivery_address)
            closest_package = package

    return closest_package
