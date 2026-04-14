class Storage:
    def __init__(self):
        self.data = []

    def add_sales(self, sales: list):
        self.data.extend(sales)
        return len(sales)

    def get_all(self):
        return self.data

db = Storage()