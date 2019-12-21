from deck import Deck
from players import Player, Common, Advanced


def create_deck(self):
    user_input = None
    valid_number = False
    while not valid_number:
        try:
            user_input = input("How many decks would you like to play with? ")
            self.number_decks = int(user_input)
            valid_number = True
        except ValueError:
            print(f"{user_input} is not a valid input. Please enter an int.")

    print(f"You are playing with {self.number_decks} decks.")

    self.cards = self.deck * self.number_decks
    return


def get_number_hands(self):
    user_input = None
    valid_number = False
    while not valid_number:
        try:
            user_input = input("How many hand would you like to play? ")
            self.number_hands = int(user_input)
            valid_number = True
        except ValueError:
            print(f"{user_input} is not a valid input. Please enter an int.")

    print(f"You are playing {self.number_hands} hands.")
    return


def record_outcome(player, dealer, bet):
    if player.total > 21:
        dealer.wins += bet
        player.balance -= bet
    elif dealer.total > 21:
        player.wins += bet
        player.balance += bet
    elif player.total < dealer.total <= 21:
        dealer.wins += bet
        player.balance -= bet
    elif dealer.total < player.total <= 21:
        player.wins += bet
        player.balance += bet
    elif dealer.total == player.total:
        bet = 0
    else:
        player.wins += bet
        player.balance += bet
    return bet


def player_turn(player, deck, upcard=None):
    player.act(upcard)
    while True:
        if player.action == 'hit':
            player.cards.append(deck.draw())
            player.act(upcard)
        elif player.action == 'stand':
            break
        elif player.action == 'double':
            player.cards.append(deck.draw())
            break
        elif player.action == 'split':  # TODO: Add splitting logic and recurse up to 4 times (max allowed splits)
            player.cards.append(deck.draw())
            player.act(upcard)
            break
    return


def main():
    number_decks = 8
    number_hands = 10000
    deck = Deck(number_decks)

    dealer = Player("dealer")
    default_player = Player("default")
    common_player = Common("common")
    advanced_player = Advanced("advanced")

    players = [default_player, common_player, advanced_player]

    print(f"Playing {number_hands} hands with {number_decks} decks.")
    for player in players:
        total_bet = 0
        dealer.wins = 0
        pushed = 0
        for hand in range(number_hands):

            # Shuffle every hand (as in online)
            deck.shuffle()
            player.cards = []
            dealer.cards = []

            bet = 1

            # Deal two cards
            for i in range(2):
                player.cards.append(deck.draw())
                dealer.cards.append(deck.draw())

            player.calculate_total()
            dealer.calculate_total()

            # blackjacks
            if dealer.total == 21 and player.total != 21:
                dealer.wins += bet
                player.balance -= bet
                total_bet += bet
                continue
            elif player.total == 21 and dealer.total != 21:
                player.wins += bet
                player.balance += bet * 1.5
                total_bet += bet
                continue
            elif player.total == dealer.total == 21:
                pushed += bet
                continue

            upcard = dealer.cards[0]

            # Player turn
            player_turn(player, deck, upcard)

            # Dealer turn
            player_turn(dealer, deck)

            player.calculate_total()
            dealer.calculate_total()

            # Record outcome
            if player.action == 'double':
                bet = bet * 2
            bet = record_outcome(player, dealer, bet)
            total_bet += bet

        # After, record stats
        # TODO: Take the limit of results to get more accurate win percent
        win_percentage = (player.wins / total_bet) * 100
        push_percentage = (pushed / number_hands) * 100

        print(f"Stats for {player.name}: ")
        print(f"    Pushed hands percentage: {push_percentage}")
        print(f"    Win percentage: {win_percentage}")
        print(f"    Net points: {player.balance}")
        print()


if __name__ == '__main__':
    main()
