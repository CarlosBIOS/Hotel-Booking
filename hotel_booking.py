import pandas as pd


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

    def is_available(self):
        """Check if the hotel is available"""
        if self.available == 'yes':
            return True
        return False


class ReservationTicket:

    def __init__(self, user, hotel):
        self.user = user
        self.hotel = hotel

    def __str__(self):
        return 'Manage, plan and verify if the user have or not a reservation'

    def generate(self):
        content = f'''
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.user}
        Hotel: {self.hotel}
        '''
        return content

    def spa_book(self, answer):
        if answer == 'yes':
            print(f'''
        Thank you for your SPA reservation!
        Here are you booking data:
        Name: {self.user}
        Hotel: {self.hotel}
        ''')
        else:
            print("Ok, so it's not booked the spa")

    @property
    def user(self):
        return self.user.strip().title()


class CreditCard:

    def __init__(self, number: str, expiration: str, holder: str, cvc: str):
        self.number: str = self._validate_input(number, 4, 'card number')
        self.expiration: str = expiration
        self.holder: str = holder
        self.cvc: str = self._validate_input(cvc, 3, 'CVC')

#  O underline na frente do nome de um método indica que ele é um método privado. Métodos privados são destinados para
#  uso interno da classe e não devem ser chamados diretamente de fora dela. No caso da classe CreditCard, o método
#  _validate_input é privado porque ele é uma função auxiliar usada internamente para validar a entrada do usuário para
#  os atributos number e cvc. Ele não faz parte da funcionalidade pública da classe CreditCard!!!!
# Não posso utilizar @staticmethod, pois permite que o método seja utilizado fora da classe, caso seja útil em outros
# contextos
    def _validate_input(self, value: str, length: int, name: str) -> str:
        while not (value.isdigit() and len(value) == length):
            value = input(f'Please, enter a valid {name} with {length} digits: ').strip()
        return value

    def validate(self) -> bool:
        # data: list = pd.read_csv('cards.csv', dtype= str).to_dict(orient='records')
        data: dict = pd.read_csv('cards.csv', dtype=str).to_dict()
        if all(getattr(self, attr) in data[attr].values() for attr in ['number', 'expiration', 'holder', 'cvc']):
            print('\nIs a valid card!')
            return True
        else:
            print('\nThere was a problem with your credit card!')
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        data = pd.read_csv('card_security.csv', dtype=str)
        password: str = data.loc[data['number'] == self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            print('Credit card authentication failed!')
            return False


def yes_or_no(answer: str) -> str:
    while answer not in ('yes', 'no'):
        answer: str = input('Please write yes or no: ').casefold().strip()
    return answer


def main():
    print('\n', pd.read_csv('hotels.csv'))

    identification: str = input('\nEnter the id of the Hotel: ').strip()
    hotel = Hotel(identification)

    if hotel.is_available():
        answer: str = yes_or_no(input('Do you want to book the hotel? ').strip().casefold())
        if answer == 'yes':
            card_number: str = input('\nPlease, enter your credit number card: ').strip()
            expiration: str = input('Please, enter the expiration of your card: ').strip()
            holder_name: str = input('Please, enter your holder name from your card: ').strip()
            cvc_number: str = input('Please, enter your csv number: ').strip()
            creditcard = SecureCreditCard(number=card_number, expiration=expiration, holder=holder_name, cvc=cvc_number)
            if creditcard.validate():
                if creditcard.authenticate(given_password=input('Please, write the password: ').strip()):
                    hotel.book()
                    reservation_ticket = ReservationTicket(holder_name.title(), hotel.name)
                    print(reservation_ticket.generate())
                    reservation_ticket.spa_book(yes_or_no(input('Do you want to book a spa package? ')
                                                          .strip().casefold()))
    else:
        print('The Hotel is not available')


if __name__ == '__main__':
    main()
