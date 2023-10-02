class Package:

    # Constructor for Package objects. Includes a truck variable that allows a package to access its
    # respective truck's methods.
    def __init__(self, id_num, deliv_add, deliv_city, deliv_zip, deliv_dead, pack_weight, deliv_status):
        self.id = id_num
        self.delivery_address = deliv_add
        self.delivery_city = deliv_city
        self.delivery_zip_code = deliv_zip
        self.delivery_deadline = deliv_dead
        self.package_weight = pack_weight
        self.delivery_status = deliv_status
        self.index_number = 0
        self.truck = ""

    # __repr__ and __str__ methods are overridden in order to display specific, relevant information concerning packages
    def __repr__(self):
        return str(self.id) + ": " + self.delivery_status

    def __str__(self):
        return str(self.id) + ": " + self.delivery_status
