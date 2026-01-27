import random
import sys
import json
import argparse
import os
from tqdm import tqdm

# -----------------------------------------------------------------------------
# Constants and Path Helpers
# -----------------------------------------------------------------------------

DATA_DIR = "data"


def get_sim_path(x):
    """
    Returns the standard path for simulation results for strategy X.
    """
    return os.path.join(DATA_DIR, f"sim_results_{x}.jsonl")


# -----------------------------------------------------------------------------
# Card and Deck Definitions
# -----------------------------------------------------------------------------


def create_deck():
    """
    Creates and returns a shuffled deck of Flip7 cards.
    """
    deck = []

    # Number cards: denomination n has count n, except 0 has count 1.
    # 0: 1
    # 1: 1
    # 2: 2
    # ...
    # 12: 12
    deck.append(0)
    for i in range(1, 13):
        deck.extend([i] * i)

    # Modifier cards
    # +2, +4, +6, +8, +10 (one of each)
    deck.extend(["+2", "+4", "+6", "+8", "+10"])

    # Double card: x2 (one)
    deck.append("x2")

    # Second Chance cards: 3 instances
    deck.extend(["SC"] * 3)

    random.shuffle(deck)
    return deck


def calculate_score(hand, is_bust=False):
    """
    Calculates the score of a hand according to Flip7 rules.
    If is_bust is True, score is 0.
    """
    if is_bust:
        return 0

    # Separate cards
    numbers = []
    modifiers = []
    has_doubler = False

    for card in hand:
        if isinstance(card, int):
            numbers.append(card)
        elif card == "x2":
            has_doubler = True
        elif isinstance(card, str) and card.startswith("+"):
            modifiers.append(int(card[1:]))
        # SC cards have no point value and stick around until used/end

    # 1. Total points from number cards
    # Check for bust (internal integrity check, though sim handles bust state)
    # The rule says: "The player busts if they have any two cards of the same denomination"
    # We assume the passed hand is valid (not busted) unless is_bust flag is True.

    base_sum = sum(numbers)

    # 2. Apply Double
    score = base_sum
    if has_doubler:
        score *= 2

    # 3. Add point modifiers
    score += sum(modifiers)

    # 4. Flip 7 Bonus
    # "If the hand contains seven cards and is not busted... 15 points"
    if len(hand) == 7:
        score += 15

    return score


# -----------------------------------------------------------------------------
# Simulation Logic
# -----------------------------------------------------------------------------


def run_simulation(strategy_x):
    """
    Runs a single simulation of Flip7 with strategy:
    "Hit until score >= strategy_x"
    Exception: If holding a Second Chance card, always hit (never stand).

    Returns a dictionary with the outcome.
    """
    deck = create_deck()
    hand = []
    has_sc = False
    is_bust = False

    while True:
        # Check end conditions

        # 1. Max cards
        if len(hand) >= 7:
            break

        current_score = calculate_score(hand)

        # 2. Strategy Check
        # Stand if score >= X, UNLESS we have a Second Chance card.
        # "One can infer that nobody would ever stand if they have a second chance card."
        if current_score >= strategy_x and not has_sc:
            break

        # Draw a card
        if not deck:
            break  # Should not happen in normal play

        card = deck.pop()

        if card == "SC":
            if has_sc:
                # Discard the new SC immediately (keep the old one)
                pass
            else:
                has_sc = True
                hand.append(card)

        elif isinstance(card, int):
            if card in hand:
                if has_sc:
                    # Saved by Second Chance!
                    # "Discard both the Second Chance card and the duplicate number card."
                    has_sc = False
                    hand.remove("SC")
                    # The new card 'card' is effectively discarded (not added to hand)
                else:
                    # Bust!
                    hand.append(card)  # Add it to capture the bust state in the record
                    is_bust = True
                    break
            else:
                hand.append(card)

        else:
            # Modifier or x2
            hand.append(card)

    final_score = calculate_score(hand, is_bust)
    is_flip_seven = len(hand) == 7 and not is_bust

    return {
        "cards": hand,
        "is_bust": is_bust,
        "total_value": final_score,
        "is_flip_seven_bonus": is_flip_seven,
    }


# -----------------------------------------------------------------------------
# IO / Validations
# -----------------------------------------------------------------------------


def save_simulations(results, x):
    """
    Appends simulation results to a JSONL file.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = get_sim_path(x)
    with open(filename, "a") as f:
        for res in results:
            f.write(json.dumps(res) + "\n")


def read_simulations(x):
    """
    Yields simulation results from a JSONL file.
    """
    filename = get_sim_path(x)
    if not os.path.exists(filename):
        return

    with open(filename, "r") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    parser = argparse.ArgumentParser(description="Run Flip7 Simulations")
    parser.add_argument(
        "X", type=int, help="Target score threshold to stand (Strategy X)"
    )
    parser.add_argument("n", type=int, help="Number of simulations to run")

    args = parser.parse_args()

    results = []
    # Optimization: Write in chunks if n is huge, but list is fine for reasonable n
    for _ in tqdm(range(args.n), desc=f"Strategy X={args.X}"):
        res = run_simulation(args.X)
        results.append(res)

    save_simulations(results, args.X)
    print(
        f"Ran {args.n} simulations with Strategy X={args.X}. Results appended to {get_sim_path(args.X)}"
    )


if __name__ == "__main__":
    main()
