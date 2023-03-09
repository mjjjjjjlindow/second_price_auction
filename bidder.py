import random

class Bidder:

    def __init__(self, num_users, num_rounds, id):
        """"""
        self._num_users = num_users
        self._num_rounds = num_rounds

        self.id = id
        self.balance = 0
        self.balance_history = []

        self._current_user = None
        self._history = {}

        self._win_history = []

        self.fixed = random.random()

        self._attempts = 0 # The number of non-zero bids.
        self._wins = 0
        self._spend = 0
        self._clicks = 0
        self._name = 'Random'

    def __repr__(self):
        """"""
        return self._name
    
    @property
    def attempts(self):
        return self._attempts
    
    @property
    def wins(self):
        return self._wins
    
    @property
    def spend(self):
        return self._spend
    
    @property
    def clicks(self):
        return self._clicks
    
    @property
    def params(self):
        return {}

    def bid(self, user_id):
        """"""
        self._current_user = self._lookup_user(user_id)
        bid = self._bid(self._current_user)
        if(bid > 0):
            self._attempts += 1
        return bid

    def _bid(self, user_history):
        """"""
        return random.random()
    
    def _lookup_user(self, user_id):
        """"""
        class UserHistory():
            def __init__(self, user_id):
                self.id = user_id
                self._rounds = 0
                self._won = []
                self._bids = []
                self._clicked = []

                self._n_wins = 0
                self._n_clicks = 0

            @property
            def rounds(self):
                return self._rounds

            @property
            def wins(self):
                return self._n_wins
            
            @property
            def clicks(self):
                return self._n_clicks
            
            @property
            def win_rate(self):
                if self.wins == 0:
                    return None
                return self.clicks / self.wins
            
            @property
            def click_rate(self):
                """The observed click-rate based on win observations."""
                if self._n_wins == 0:
                    return 0
                return self._n_clicks / self._n_wins
            
            @property
            def max_rate(self):
                """The maximum historical rate for the customer."""
                if self._rounds == 0:
                    return 0
                return max(self._bids)
            
            @property
            def market_rate(self):
                """The click-rate the market expects based on average bid data."""
                if self._rounds == 0:
                    return 0
                return sum(self._bids) / len(self._bids)

            @property
            def weighted_market_rate(self):
                """The click-rate the market expects weighted for more recent value."""
                if self._rounds == 0:
                    return 0
                factor = 2
                cum_weight = 0
                sum_weight = 0
                for i, val in enumerate(self._bids):
                    weight = factor ** i
                    cum_weight += weight
                    sum_weight += val * weight
                return sum_weight / cum_weight

            @property
            def latest_market_rate(self):
                """The click-rate the market expects, based on the last auction round."""
                return self._bids[-1]

            def notify(self, won, price, clicked=None):
                self._rounds += 1
                self._won.append(won)
                self._bids.append(price)
                self._clicked.append(clicked)
                if won:
                    self._n_wins += 1
                if clicked:
                    self._n_clicks += 1

            def nPrice(self, n):
                """Return the past n auction prices."""
                return self._bids[-n:]
            
            def nAvg(self, n):
                """Return the average price for the past n auctions."""
                bids = self.nPrice(n)
                if len(bids) == 0:
                    return 0
                return sum(bids) / len(bids)

        if user_id in self._history:
            return self._history[user_id]
        history = UserHistory(user_id)
        self._history[user_id] = history
        return history

    def notify(self, auction_winner, price, clicked=None):
        """"""
        self._current_user.notify(auction_winner, price, clicked)
        if auction_winner == True:
            self._win_history.append(1)
            self.balance -= price
            self._wins += 1
            self._spend += price
            if clicked == True:
                self.balance += 1
                self._clicks += 1
        else:
            self._win_history.append(0)
        self.balance_history.append(self.balance)

   
class AddaptiveBidder(Bidder):

    def __init__(self, num_users, num_rounds, id):
        super().__init__(num_users, num_rounds, id)
        self._expected = 0.5 # The expected value with no other information.
        self._blend_rate = random.randint(20, 50)
        self._factor = random.uniform(0.9, 1.15)
        self._back = random.randint(1, 30)
        self._threshold = random.uniform(0.2, 0.8)
        self._name = f'AddaptiveBidder ({self._blend_rate}, {self._back}, {self._threshold})'

    @property
    def params(self):
        return {
            'name': 'Addaptive',
            'blend_rate': self._blend_rate,
            'lookback': self._back,
            'threshold': self._threshold,
        }

    def _bid(self, user_history):
        """Start with the default expected value and update it over time with past information."""
        wins = user_history.wins
        expected = self._expected
        if self.balance < -10:
            self._factor = random.uniform(0.9, 1.1)
        back = self._win_history[-self._back:]
        if len(back) > 0 and sum(back) / len(back) < self._threshold:
            self._factor = min(1.1, self._factor * random.uniform(1, 1.02))

        factor = self._factor
        if wins == 0:
            return  expected * factor
        win_rate = user_history.win_rate
        n = self._blend_rate
        if wins < n:
            t = wins / n
            return (t * win_rate + expected * (1 - t)) * factor # Blend between rates.
        else:
            return win_rate * factor

def getBidders(n_users, n_rounds, n):
    """Return a list of n randomly selected bidders."""
    options = [Bidder, AddaptiveBidder]
    weights = [1, 100]
    bidders = []
    for i in range(n):
        bidder = random.choices(options, weights)[0]
        bidders.append(bidder(n_users, n_rounds, i))
    return bidders
