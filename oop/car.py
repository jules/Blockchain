from vehicle import Vehicle


class Car(Vehicle):
    # top_speed = 150
    # warnings = []

    def brag(self):
        print('Look how cool my car is!')


lambo = Car()
lambo.drive()

# Car.top_speed = 200
lambo.add_warning('New warning')
print(lambo)

ferrari = Car(200)
ferrari.drive()
print(ferrari.get_warnings())

vw = Car(100)
vw.drive()
print(vw.get_warnings())
