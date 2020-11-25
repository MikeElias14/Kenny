from deck import Deck
from players import Dealer, Common, Advanced

from globals import (
    hit,
    stand,
    split,
    double,
    facecards,
    ace
)


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
        dealer.wins += 1
        player.balance -= bet
        player.won_previous = False
    elif dealer.total > 21:
        player.wins += 1
        player.balance += bet
        player.won_previous = True
    elif player.total < dealer.total <= 21:
        dealer.wins += 1
        player.balance -= bet
        player.won_previous = False
    elif dealer.total < player.total <= 21:
        player.wins += 1
        player.balance += bet
        player.won_previous = True
    elif dealer.total == player.total:
        bet = 0
    else:
        player.wins += 1
        player.balance += bet
    return bet


def player_turn(player, deck, upcard=None):
    player.act(upcard)
    turn_over = False
    while not turn_over:
        if player.action == hit:
            player.cards.append(deck.draw())
            player.act(upcard)
        elif player.action == stand:
            turn_over = True
        elif player.action == double:
            player.cards.append(deck.draw())
            turn_over = True
        elif player.action == split:  # TODO: Add splitting logic and recurse up to 4 times (max allowed splits)
            player.cards.append(deck.draw())
            player.act(upcard)
            turn_over = True
    return


def main():
    number_decks = 8
    number_hands = 10000
    deck = Deck(number_decks)

    players = [
        Common("common"),
        Advanced("advanced")
    ]

    dealer = Dealer("dealer")

    print(f"Playing {number_hands} hands with {number_decks} decks.")
    for player in players:
        dealer.wins = 0
        pushed = 0
        bet = 1
        for hand in range(number_hands):

            # Shuffle every hand (as in online)
            deck.shuffle()
            player.cards = []
            dealer.cards = []

            # Betting strategy
            # if not player.won_previous:
            #     bet *= 2
            # else:
            #     bet = 1

            if bet > player.largest_bet:
                player.largest_bet = bet

            # Deal two cards
            for i in range(2):
                player.cards.append(deck.draw())
                dealer.cards.append(deck.draw())

            upcard = dealer.cards[0]

            # Player turn
            player_turn(player, deck, upcard)

            # Dealer turn
            player_turn(dealer, deck)

            player.calculate_total()
            dealer.calculate_total()

            # blackjacks
            if dealer.total == 21 and player.total != 21:
                dealer.wins += 1
                player.balance -= bet
                player.won_previous = False
                continue
            elif player.total == 21 and dealer.total != 21:
                player.wins += 1
                player.balance += bet * 1.5
                player.won_previous = True
                continue
            elif player.total == dealer.total == 21:
                pushed += 1
                continue

            # Record outcome
            if player.action == 'double':
                bet *= 2
            bet = record_outcome(player, dealer, bet)

        # After, record stats
        # TODO: Take the limit of results to get more accurate win percent
        win_percentage = (player.wins / number_hands) * 100
        push_percentage = (pushed / number_hands) * 100

        print(f"Stats for {player.name}: ")
        print(f"    Pushed hands percentage: {push_percentage}")
        print(f"    Win percentage: {win_percentage}")
        print(f"    Final Balance: {player.balance}")
        print(f"    Largest Bet: {player.largest_bet}")
        print()


if __name__ == '__main__':
    main()
