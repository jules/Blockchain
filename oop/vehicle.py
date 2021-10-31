class Vehicle:
    def __init__(self, starting_top_speed=150):
        self.top_speed = starting_top_speed
        self.__warnings = []

    def __repr__(self):
        print('Printing...')
        return f'Top speed: {self.top_speed}, Warnings: {len(self.__warnings)}'

    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings

    def drive(self):
        print(f'I am driving at a top speed of {self.top_speed} km/h')