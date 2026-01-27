# flip7
Some quick code to think through Flip7 strategy

## Rules

Flip 7 is a game like black jack where you may hit or stand with each hand.  Your goal is to maximize points; over the course of many hands, the goal is to get to 200 points before you opponents.

The deck contains cards with denominations between 0 and 12, with the following counts (number of times each card appears in the deck):

| Denomination | Count |
|--------------|-------|
|            0 |     1 |
|            1 |     1 |
|            2 |     2 |
|            3 |     3 |
|            4 |     4 |
|            5 |     5 |
|            6 |     6 |
|            7 |     7 |
|            8 |     8 |
|            9 |     9 |
|           10 |    10 |
|           11 |    11 |
|           12 |    12 |

A player may continue to hit until they have seven cards or until they have busted.  The player busts if they have any two cards of the same denomination in their hand.  A busted hand is worth zero points.  Other hands are worth the sum of the cards in the hand.  If the hand contains seven cards and is not busted, then the hand gets a 15 points "Flip 7" bonus.

In addition to these cards there are modifier cards.  There are one of each of these:
 - Plus cards: +2, +4, +6, +8, +10
 - Double card: x2

If you acquired any point Modifier cards, you will first total the points you scored from number cards.  If you have the X2 Modifier card, you will double the points from the number cards.  Finally you will add any point Modifier cards to your score.  (The Flip 7 bonus gets applied after the modifiers.)

Finally there are 3 Second Chance cards in the deck.  Whenever you receive a Second Chance card, you will keep it.  Should you bust during the course of the hand, you can play the Second Chance card in order to avoid busting.  You will discard both the Second Chance card and the duplicate number card.  (One can infer that nobody would ever stand if they have a second chance card.)  You can only have one Second Chance card at a time.  If you receive a second Second Chance card, you must discard it.

Note:  In the real game, there are two other special cards that we will ignore for the sake of the analysis.

### Simplifying assumptions

Firstly, we ignore the few ways that other players may affect the main player's play, including the two special cards we have excluded.

Generally having cards of high denomination increase the probability of a bust.  Similarly having multiple, low-denomination cards increases the probability of a bust.  In order to make a easy-to-follow strategy, we will assume that players strictly follow the strategy, "Hit until your hand has value X or higher, then stand."  We call this strategy "STRAT(X)", and our goal is to determine the optimal X.

## Simulation structure

The root of simulations will be a program, sim.py, that, when run, `python sim.py <X> <n>` will run n simulations with the above rules, and save the outcomes to some file to be read later.  A simulation outcome should save the cards that were drawn, along with some precomputed fields like `is_bust`, `total_value`, `is_flip_seven_bonus`.  Other fields can be calculated on-the-fly from the cards that are saved.

sim.py should also contain functions to read the set of simulations later when needed.  The idea is that I will run `python sim.py` with lots of values of X depending on how many free cycles my computer has, then I will use these simulations to do calculations later.

