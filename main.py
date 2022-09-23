import time
import random


class Player:
    def __init__(self, name):
        self.name: str = name
        self.bets: int = 0
        self.total_sum: int = 0
        self.chips: int = 500
        self.hand: list[Card] = []
        self.still_in: bool = True

    def get_total_sum(self):
        '''
        calculates total sum of player's hand
        '''
        total = 0
        aces = 0
        print(f"{self.name}'s CARDS")
        for card in self.hand:
            print(f"{card.index} Of {card.suit}: {card.value}")
            total += card.value
            if card.index == "Ace":
                aces += 1

        while True:
            if total <= 21:
                self.total_sum = total
                return (f"TOTAL SUM: {self.total_sum}")
            else:
                Player.check_for_aces(self, total, aces)

    def get_total_sum_no_print(self):
        '''
        calculates total sum of player's hand
        '''
        total = 0
        aces = 0
        for card in self.hand:
            total += card.value
            if card.index == "Ace":
                aces += 1

        while True:
            if total <= 21:
                self.total_sum = total
                return
            else:
                Player.check_for_aces(self, total, aces)

    def check_for_aces(self, total, aces):
        '''
        checks if player has aces in hand prior to busting
        '''
        if total > 21 and aces > 0:
            for card in self.hand:
                if card.index == "Ace":
                    card.value -= 10
                    Player.get_total_sum(self)
        else:
            print(f"{self.name} has BUSTED!")
            self.still_in = False
            return

    def print_cards(self):
        total = 0
        print(f"{self.name}'s CARDS")
        for card in self.hand:
            print(f'''
{card.index}: {card.value}''')
            total += card.value
        print(f"TOTAL SUM: {total}")


class Card:
    def __init__(self, index, suit):
        self.index: str = index
        self.suit: str = suit
        self.value: int = cardvalues[index]


cardvalues = {
    "Ace": 11,
    "Jack": 10,
    "King": 10,
    "Queen": 10,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
}
DECK: list[Card] = []


def create_deck(cardvalues: dict[str, int]) -> list[Card]:
    for index in cardvalues:
        for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            DECK.append(Card(index, suit))


def get_player_amount() -> int:
    while True:
        amount = int(input('''
How many people will be playing? [Min 1, Max 7]: \n''')) 
        if not 1 <= amount <= 7:
            print("Invalid Input")
            continue
        break

    return amount


def get_player_names(amount):
    players: list[Player] = []
    for i in range(1, amount + 1):
        while True:
            name = input(f'''
Player #{i}, What Is Your Name?\n''').title()
            check = input(f'''
Is "{name}" correct? [Y/N]\n''').upper()

            if check != "Y":
                print("Unsuccessful, please re-input your name.")
                continue
            else:
                print(f"Welcome to Blackjack {name}!")
                players.append(Player(name))
                break

    return players


def bets(players: list[Player]):
    for player in players:
        while True:
            bet = int(input(f'''
{player.name}, place your bet.
[Minimum bet amount is 10]\n'''))
            if 10 <= bet <= player.chips:
                player.bets = bet
                player.chips -= bet
                break
            print("INVALID AMOUNT")
            continue


def draw_cards(players: list[Player], dealer: Player):
    for player in players:
        card = random.choice(DECK)
        DECK.remove(card)
        player.hand.append(card)
        print(f'''
{player.name} has drawn a {card.index} of {card.suit} for their FIRST card!
''')
        time.sleep(2)

    card = random.choice(DECK)
    DECK.remove(card)
    dealer.hand.append(card)
    print(f'''
{dealer.name} takes a card...''')
    time.sleep(2)

    for player in players:
        card = random.choice(DECK)
        DECK.remove(card)
        player.hand.append(card)
        print(f'''
{player.name} has drawn a {card.index} of {card.suit} for their SECOND card!
''')
        Player.get_total_sum(player)
        time.sleep(2)

    card = random.choice(DECK)
    DECK.remove(card)
    dealer.hand.append(card)
    print(f'''
{dealer.name} has drawn a {card.index} of {card.suit} for their SECOND card!
''')
    time.sleep(2)


def blackjack_after_draw(players: list[Player]):
    for player in players:
        if player.total_sum == 21:
            print(f'''
{player.name} has gotten a BLACKJACK!!
PAYOUT: {player.bets * 3}''')
            player.chips += player.bets * 3
            player.still_in = False


def hit_or_stand(players: list[Player]):
    for player in players:
        while True:
            if not player.still_in:
                break

            Player.print_cards(player)
            option = input(f'''
{player.name}, would you like to HIT or STAND?\n''').upper()
            if option != "HIT" and option != "STAND":
                print("INVALID INPUT")
                continue
            elif option == "HIT":
                print(f"{player.name} has chosen to HIT!")
                card = random.choice(DECK)
                DECK.remove(card)
                player.hand.append(card)
                print(f'''
{player.name} has drawn a {card.index} of {card.suit}!''')
                Player.get_total_sum(player)
                time.sleep(2)
                continue
            else:  # STAND
                print(f"{player.name} has chosen to STAND!")
                break


def players_vs_dealer(players: list[Player], dealer: Player):
    print(f"The {dealer.name} reveals their cards...")
    Player.get_total_sum(dealer)
    while dealer.total_sum <= 16:
        card = random.choice(DECK)
        DECK.remove(card)
        dealer.hand.append(card)
        print(f'''The {dealer.name} draws a {card.index} or {card.suit}''')
        Player.get_total_sum_no_print(dealer)

    for player in players:
        if player.still_in:
            if player.total_sum == dealer.total_sum:
                print(f'''
{player.name}'s Total: {player.total_sum}
{dealer.name}'s Total: {dealer.total_sum}
{player.name} has TIED the {dealer.name}!''')
                player.chips += player.bets
                player.still_in = False
            elif player.total_sum > dealer.total_sum:
                print(f'''
{player.name}'s Total: {player.total_sum}
{dealer.name}'s Total: {dealer.total_sum}
{player.name} has WON {player.bets * 2}!''')
                player.chips += player.bets * 2
            else:
                print(f'''
{player.name}'s Total: {player.total_sum}
{dealer.name}'s Total: {dealer.total_sum}
{player.name} has LOST!''')
        player.still_in = False


def results(players: list[Player]):
    for player in players:
        print(f'''
{player.name}'s Total Chips: {player.chips}''')
        time.sleep(1)


def reset(players: list[Player], dealer: Player):
    dealer.hand = []
    dealer.total_sum = 0
    for player in players:
        player.still_in = True
        player.bets = 0
        player.total_sum = 0
        player.hand = []


def play_again():
    while True:
        answer = input("Would you like to play again? [Y/N]\n").upper()
        if answer == 'Y':
            return True
        elif answer == 'N':
            return False
        else:
            print("INVALID RESPONSE")


def main():
    global DECK
    amount = get_player_amount()
    players = get_player_names(amount)
    dealer = Player("Dealer")
    while play_again:
        create_deck(cardvalues)
        bets(players)
        draw_cards(players, dealer)
        blackjack_after_draw(players)
        hit_or_stand(players)
        players_vs_dealer(players, dealer)
        results(players)
        play_again()
        reset(players, dealer)
        DECK.clear()


main()
