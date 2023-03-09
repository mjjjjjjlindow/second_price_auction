# %%
import os
import random
import pandas as pd
from auction import User, Auction
from bidder import getBidders, AddaptiveBidder



def run_auction():
    """Run a single auction."""
    n_users = random.randint(2, 1000)
    n_bidders = random.randint(5, 50)
    n_rounds = random.randint(100, 10000)

    users = [User(i) for i in range(0, n_users)]
    bidders = getBidders(n_users, n_rounds, n_bidders)
    auction = Auction(users, bidders)
    for _ in range(0, n_rounds):
        auction.execute_round()
    return auction

def run_auctions(n):
    """Run multiple auctions."""
    data = []
    'RUNNIN AUCTIONS'
    for i in range(n):
        print(f'\r  AUCTION: {i}', end='')
        auction = run_auction()
        data.append(get_auction_data(i, auction))
    print()
    return pd.DataFrame(data)

def get_auction_data(i, auction):
    """Format the results of the simulation to a pandas DataFrame."""
    winner = auction.winner
    n = None
    f = None
    isAddaptive = isinstance(winner, AddaptiveBidder)
    if isAddaptive:
        n = winner.wait
        f = winner.factor
    return  {
        'auction': i,
        'rounds': auction.rounds,
        'users': len(auction.users),
        'bidders': len(auction.bidders),
        'is_addaptive': isAddaptive,
        'wait': n,
        'factor': f,
        'clicks': winner.clicks,
        'wins': winner.wins,
        'balance': winner.balance,
        'attempts': winner.attempts,
    }

if __name__ == '__main__':
    # auction = run_auction()
    # auction.plot_history(legend=False)
    # auction.display_bidders()
    # auction.display_summary()

    df = run_auctions(50)
    curr_dir = os.path.dirname(__file__)
    filepath = os.path.join(curr_dir, 'data.pickle')
    df.to_pickle(filepath)
