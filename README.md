# Black-jack
Simulation of playing thousands or millions of hands of blackjack at a casino to find out the expected value of dealer wins and other stats.

Have you ever wondered what would happen in the long run if you played Blackjack at a casino, "by the Blackjack chart/table"?

Blackjack chart tells the player exactly what to do for every possible scenario a player could have. In this project this player decision is placed into two charts.
The hit_stay_or_double.csv chart and the splitting.csv chart.
The hit_stay_or_double chart takes two inputs, the player total (soft and hard total) and the dealer up-card, and returns either hit, stay, or double.  
If the player is dealt a pair as the original hand, then the splitting chart is used (along with the dealer up-card) to decide split or stay.

In this version of Blackjack the dealer plays as follows:
  17 or above, the dealer must stand.
  16 or below, the dealer must keep hitting until the dealer is at or above 17.
  If dealer has an ace and counting it as 11 puts the dealer at or above 17 without busting, then the dealer must stand.
  
Splitting is only allowed by the players and only on the original hand.

After running the simulation a dealers-stats-pie-chart is created. I am getting the following results:
- dealer wins about 48% of the time.
- dealer loses about 43% of the time.
- dealer pushes about 8% of the time.

players_balance.png is created at the end as well. This shows how each player's balance changes thru-out. How the winning/losing happens over time. I was thinking that if the deck favors the player or if the deck favors the players then I would see all the players losing/winning together. I don’t see this trend.

inputs in this simulation. number of rounds and number of players at the table.

Each player bets $10 for each hand.
If a player gets a natural Blackjack, then the dealer pays 1.5 times the bet, so $15.

My finds are contrary to what I hear about some only 0.5% house-advantage if you play by the chart. 
  
