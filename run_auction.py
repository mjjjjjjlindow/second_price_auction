# %%
import os
import random
import pandas as pd
from auction import User, Auction
from bidder import getBidders



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
    params = winner.params
    data = {
        'auction': i,
        'rounds': auction.rounds,
        'users': len(auction.users),
        'bidders': len(auction.bidders),
        'clicks': winner.clicks,
        'wins': winner.wins,
        'balance': winner.balance,
        'attempts': winner.attempts,
    }
    data.update(params)
    return data

if __name__ == '__main__':
    # Reload poject modules to 'hot-reload' while using vscode interactive terminal.
    import importlib
    modules = ['auction', 'bidder']
    for module in modules:
        importlib.reload(__import__(module))

    single = True
    if single:
        auction = run_auction()
        auction.plot_history(legend=False)
        auction.display_bidders()
        auction.display_summary()
    else:
        df = run_auctions(50)
        try:
            curr_dir = os.path.dirname(__file__)
        except:
            # Executing in the iPython terminal.
            curr_dir = os.getcwd()
        filepath = os.path.join(curr_dir, 'data.pickle')
        if os.path.exists(filepath):
            data = pd.read_pickle(filepath)
            data = pd.concat([data, df])
            data.to_pickle(filepath)
        else:
            df.to_pickle(filepath)
