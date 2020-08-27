import random

suits = ('Corazones', 'Diamantes', 'Picas', 'Tréboles')
ranks = ('Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete',
         'Ocho', 'Nueve', 'Diez', 'Sota', 'Reina', 'Rey', 'As')
values = {'Dos': 2, 'Tres': 3, 'Cuatro': 4, 'Cinco': 5, 'Seis': 6, 'Siete': 7, 'Ocho': 8,
          'Nueve': 9, 'Diez': 10, 'Sota': 10, 'Reina': 10, 'Rey': 10, 'As': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} de {self.suit}'


class Deck:

    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def __str__(self):
        cards = ""
        for card in self.cards:
            cards += str(card) + "\n"
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()


class Player:

    def __init__(self, name):
        self.name = name
        self.bankroll = 100
        self.hand = []

    def add_money(self, amount):
        self.bankroll += amount

    def remove_money(self, amount):
        if amount > self.bankroll:
            return "¡No hay esa cantidad de plata!"
        self.bankroll -= amount

    def hit(self, deck):
        self.hand.append(deck.deal_one())

    def hand_value(self):
        aces_count = 0
        total_sum = 0
        for card in self.hand:
            if card.value != 11:
                total_sum += card.value
            else:
                aces_count += 1

        if aces_count > 0:
            for i in range(aces_count):
                if total_sum + 11 <= 21:
                    total_sum += 11
                else:
                    total_sum += 1
        return total_sum


def print_hand(player, round=""):
    print("\nTu mano:" if player.name ==
          human.name else "\nLa mano de EL DEALER:")
    if player.name == "EL DEALER" and round == "1st":
        print(f"{dealer.hand[0]}"
              "\nLa otra carta está boca abajo."
              f"\nValor total: {dealer.hand[0].value} + ¿?")
    else:
        for card in player.hand:
            print(card)
        print(f"Valor total: {player.hand_value()}")


def deal_cards(n):
    for i in range(n):
        human.hit(deck)
        dealer.hit(deck)


def play_again(ask):
    output = {"s": True, "n": False}
    answer = input(f'{ask}').lower()
    while answer not in ["s", "n"]:
        answer = input(
            '\nNo entendí. Tipeá S si la respuesta es sí y N si la respuesta es no.').lower()
    return output[answer]


# Game Setup
print('\n\nAntes que nada, ¿cómo es tu nombre?')
human = Player(input('\nIngresá tu nombre: ').upper())
dealer = Player("EL DEALER")

deck = Deck()
deck.shuffle()

print(f'\n¡{human.name}! Qué nombre tan agradable. Muy bien, empecemos sin más.')
input('\n[Enter para continuar]')

# Game on
games = 0

while True:
    print(f"CANTIDAD DE CARTAS EN EL MAZO: {len(deck.cards)}")
    # check if no more money or cards:
    if human.bankroll == 0:
        print("\n¡No tenés más plata para apostar! ¡Se terminó el juego!"
              f"\n\nTerminaste con ${human.bankroll}. Deberías vender el auto y jugar de nuevo.\n")

        if not play_again(ask='¿Querés jugar de nuevo? S/N'):
            print("\n\n\n¿Justo ahora vas a abandonar? ¿Y si la próxima te iba bien?\n")
            break
        human.bankroll = 75 - games * 2
        deck.__init__()
        games += 1

        if human.bankroll < 1:
            print("\n\n¡No tenés más plata para jugar! ¡Todo terminó!\n")
            if not play_again(ask='¿Estarías interesado en vender algún órgano para seguir jugando? S/N'):
                print("\nEs entendible. Al fin y al cabo, mantener los órganos en su lugar "
                      "también nos permite seguir apostando, ¿no?\n")
                break
            human.bankroll = 1000
            deck.__init__()
            games += 1
            print(
                f"\nVendiste un órgano y ahora tenés ${human.bankroll}, ¡excelente decisión, felicidades!")
            input("\n[Enter para continuar]")

    if len(deck.cards) < 13:
        print("\nNo hay suficientes cartas para seguir jugando. ¡Se terminó el juego!"
              f"\n\nTerminaste con ${human.bankroll}. Recordá seguir apostando sin importar cuánto pierdas.\n")

        if not play_again(ask='¿Querés jugar de nuevo? S/N'):
            break
        human.bankroll += 25 + games * games
        deck.__init__()
        games += 1

    # placing the bet
    bet = 0
    betting = True
    while betting:
        try:
            bet = int(
                input(f"\nTenés ${human.bankroll}. Ingresá el monto que querés apostar: "))
        except:
            print("\nPerdón, sólo acepto números enteros.")
        if bet > 0 and bet <= human.bankroll:
            break
        else:
            print(
                f"\nTenés que apostar más de $0 y no más de ${human.bankroll}.")

    print(f'\nTu apuesta es de ${bet}.')

    # round on
    round_on = True
    round_result = "..."

    # card dealing
    deal_cards(2)
    print_hand(human)
    input('\n[Enter para ver la mano de EL DEALER]')
    print_hand(dealer, round="1st")

   # human's turn
    while round_on:

        if human.hand_value() > 21:
            print("\n¡Te pasaste de los 21! Esta vez gana EL DEALER.")
            round_result = "dealer wins"
            round_on = False
            break

        if human.hand_value() == 21:
            break

        next_move = ""
        while next_move not in ["otra", "listo"]:
            next_move = input(
                "\nSi querés otra carta, tipeá OTRA. Si no, tipeá LISTO: ").lower()

        if next_move == "otra":
            human.hit(deck)
            print_hand(human)

        if next_move == "listo":
            print("\nLe toca a EL DEALER.")
            break

    input("\n[Enter para continuar]")

    # dealer's turn
    while round_on:
        print("\nEL DEALER reveló la carta que tenía boca abajo.")
        print_hand(dealer)

        input("\n[Enter para continuar]")

        while dealer.hand_value() < human.hand_value():
            dealer.hit(deck)
            print(
                f"\nEL DEALER robó otra carta: {dealer.hand[-1]}.")
            print_hand(dealer)

            if dealer.hand_value() > 21:
                print(f"\n¡EL DEALER se pasó de los 21! ¡Gana {human.name}!")
                round_result = "human wins"
                round_on = False
                break
            input("\n[Enter para continuar]")
        break

    # compare hands
    if round_on:
        if human.hand_value() > dealer.hand_value():
            print(f"\n¡Gana {human.name}!")
            round_result = "human wins"
            input("\n[Enter para continuar]")
        elif human.hand_value() < dealer.hand_value():
            print("\n¡Gana EL DEALER!")
            round_result = "dealer wins"
            input("\n[Enter para continuar]")
        else:
            print("\n¡Empate!")
            round_result = "tie"
            input("\n[Enter para continuar]")

    # collect bet
    if round_result == "human wins":
        human.add_money(bet)
    elif round_result == "dealer wins":
        human.remove_money(bet)

    # empty player hands
    human.hand = []
    dealer.hand = []
