class Remote:
    def __init__(self, type, brand, name):
        self.type = type
        self.brand = brand
        self.name = name

class Device(Remote):
    def __init__(self, type, brand, name, location, power, add_date):
        super().__init__(type, brand, name)
        self.location = location
        self.power = power
        self.add_date = add_date

class Device_Usage(Remote):
    def __init__(self, type, brand, name, add_date, use_count, electricity_dict, add_date_days=0):
        super().__init__(type, brand, name)
        self.add_date = add_date
        self.add_date_days = add_date_days
        self.use_count = use_count
        self.electricity_dict = electricity_dict
