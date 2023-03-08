# %%
import random
from auction import User, Auction
from bidder import getBidders


n_users = random.randint(2, 1000)
n_bidders = random.randint(5, 30)
n_rounds = random.randint(100, 1000)

users = [User(i) for i in range(0, n_users)]
bidders = getBidders(n_users, n_rounds, n_bidders)
auction = Auction(users, bidders)
for _ in range(0, n_rounds):
    auction.execute_round()

auction.plot_history(legend=False)
auction.display_bidders()
auction.display_summary()
