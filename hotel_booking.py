import pandas as pd


class User:

    def __init__(self, name: str, password: str):
        self.name: str = name
        self.password: str = password

    def __str__(self):
        return 'Creates a User class'


class Hotel:

    def __init__(self, identification: str):
        while True:
            try:
                self.identification: int = int(identification)
                break
            except ValueError:
                identification: str = input('Please write a valid form of id: ').strip()
        self.data = pd.read_csv('hotels.csv')
        self.name: str = self.data.loc[self.data['id'] == self.identification, 'name'].squeeze()
        self.city: str = self.data.loc[self.data['id'] == self.identification, 'city'].squeeze()
        self.capacity: int = self.data.loc[self.data['id'] == self.identification, 'capacity'].squeeze()
        self.available: str = self.data.loc[self.data['id'] == self.identification, 'available'].squeeze()

    def __str__(self):
        return 'Deal with hotels problems'

    def book(self):
        """Book a hotel by changing its availability to no"""
        self.data.loc[self.data['id'] == self.identification, 'available'] = 'no'
        self.data.to_csv('hotels.csv', index=False)
        print('Is booked')

    def is_available(self):
        """Check if the hotel is available"""
        try:
            if self.available == 'yes':
                return True
            return False

        except ValueError:
            return ''


class ReservationTicket:

    def __init__(self, user, hotel):
        self.user = user
        self.hotel = hotel

    def __str__(self):
        return 'Manage, do and verify if the user have or not a reservation'

    def generate(self):
        content = f'Name of the custumer hotel {self.user}'
        return content


def main():
    identification: str = input('Enter the id of the Hotel: ').strip()

    user = User('carlos', '')
    hotel = Hotel(identification)

    if hotel.is_available():
        hotel.book()
        reservation_ticket = ReservationTicket(user, hotel.name)
        print(reservation_ticket.generate())
    else:
        print('The Hotel is not available')


if __name__ == '__main__':
    main()
