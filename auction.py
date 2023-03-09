import random
from matplotlib import pyplot as plt


class Auction:
    def __init__(self, users, bidders):
        """"""
        self.users = users
        self.bidders = bidders
        self.rounds = 0

    def __repr__(self):
        """"""
        return f'Auction (Users: {len(self.users)}, Bidders: {len(self.bidders)})'

    def execute_round(self):
        """"""
        user = random.choice(self.users)
        user_id = user.id
        clicked = user.show_ad()

        bids = [(b, b.bid(user_id)) for b in self.bidders]
        max_bid = max([b[1] for b in bids])
        price_options = [b[1] for b in bids if b[1] < max_bid]
        if len(price_options) == 0:
            price = max_bid
        else:
            price = max(price_options)
        potential_winners = [b[0] for b in bids if b[1] == max_bid]
        winner = random.choice(potential_winners)
        for [bidder, _] in bids:
            if bidder.id == winner.id:
                bidder.notify(True, price, clicked)
            else:
                bidder.notify(False, price, None)
        self.rounds += 1

    def plot_history(self, legend=True):
        """"""
        rounds = [i for i in range(0, self.rounds)]
        for bidder in self.bidders:
            balance = bidder.balance_history
            plt.plot(rounds, balance, label=str(bidder))

        plt.title('Balances Over Time')
        plt.xlabel('Round')
        plt.ylabel('Balance')
        if(legend):
            plt.legend()
        plt.show()

    def display_summary(self):
        """Print a summary of the auction."""
        print('SUMMARY')
        print('Users:', len(self.users))
        print('Bidders:', len(self.bidders))
        print('Rounds:', self.rounds)
        print('Rounds/User:', self.rounds / len(self.users))
        print()

    def display_bidders(self):
        """Print an the bidders in rank order."""
        self.bidders.sort(key=lambda x : x.balance, reverse=True)
        print('BIDDER RANKING')
        print('Rank      Balance   Attempts    Clicks/Wins   Profit/Win   Bidder')
        print('---------------------------------------------------------')
        for i, bidder in enumerate(self.bidders):
            balance = bidder.balance
            attempts = bidder.attempts
            clicks = bidder.clicks
            wins = bidder.wins
            value = 0 if balance == 0 else balance / wins
            v = f'{value:.2f}'
            ratio = str(clicks) + ' / ' + str(wins)
            print(f'{i:4d}   {balance:10.2f}      {attempts:5d}   {ratio:>12}       {v:>6}   {bidder}')
        print('---------------------------------------------------------')
        print()

    @property
    def winner(self):
        self.bidders.sort(key=lambda x: x.balance, reverse=True)
        return self.bidders[1]


class User:
    def __init__(self, id):
        """"""
        self.id = id
        self.__p = random.random()

    def __repr__(self):
        """"""
        return f'User #{self.id}: {self.__p}'

    def show_ad(self):
        """"""
        return random.random() < self.__p