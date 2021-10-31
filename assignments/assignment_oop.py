# 1. Create a Food class with a "name" and a "kind" attribute as well as a "describe()" method
# which prints "name" and "kind" in a sentence
class Food:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return str(self.__dict__)

    def describe(self):
        print(f'I have {self.name}, which is a kind of {self.kind}.')


# 2. Create a "Meat" and a "Fruit" class - both should inherit from "Food". Add a "cook()" method
# to Meat and "clean()" to Fruit.


class Meat(Food):
    def __init__(self, name):
        super().__init__(name, 'Meat')

    def cook(self):
        print(f'We are cooking some {self.name}.')


class Fruit(Food):
    def __init__(self, name):
        super().__init__(name, 'Fruit')

    def clean(self):
        print(f'We are washing a {self.name}.')


maple_syrup = Food('Maple Syrup', 'Candy')
chicken = Meat('Ribs')
banana = Fruit('Banana')

maple_syrup.describe()
chicken.describe()
banana.describe()

chicken.cook()
banana.clean()

print(maple_syrup)
print(chicken)
print(banana)
