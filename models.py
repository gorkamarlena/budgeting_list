import json


class Expenses:
    def __init__(self):
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []

    def all(self):
        return self.expenses

    def get(self, id):
        expenses = [expenses for expenses in self.all() if expenses['id'] == id]
        if expenses:
            return expenses[0]
        return []

    def create(self, data):
        self.expenses.append(data)
        self.save_all()

    def save_all(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f, default=str)

    def update(self, id, data):
        record = self.get(id)
        if record:
            index = self.expenses.index(record)
            self.expenses[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        record = self.get(id)
        if record:
            self.expenses.remove(record)
            self.save_all()
            return True
        return False


expenses = Expenses()