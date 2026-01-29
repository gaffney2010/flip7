"""
multisim.py - Backwards induction to find optimal Flip7 strategies for two-player game.

For each game state (player_score, opponent_score) rounded to nearest 10s,
determines the best STRAT(X) for player 1 using simulation.
"""

import json
import os
from collections import defaultdict
from tqdm import tqdm

from sim import run_simulation, DATA_DIR

# Strategy parameters
X_VALUES = list(range(0, 101, 5))  # 0, 5, 10, ..., 100
SCORE_STEPS = list(range(0, 200, 10))  # 0, 10, 20, ..., 190
SIMS_PER_STRATEGY = 10000
WIN_THRESHOLD = 200


def round_to_10(score):
    """Round score down to nearest 10, capped at 190."""
    return min(190, (score // 10) * 10)


def simulate_hand(strategy_x):
    """Run a single hand simulation and return the score."""
    result = run_simulation(strategy_x)
    return result["total_value"]


def evaluate_strategy(p1_score, p2_score, p1_x, p2_x, win_probs, optimal_strategies, n_sims):
    """
    Evaluate player 1's win rate when starting at (p1_score, p2_score)
    with P1 using STRAT(p1_x) and P2 using STRAT(p2_x).

    Uses precomputed win_probs for states we haven't reached terminal yet.
    """
    wins = 0

    for _ in range(n_sims):
        # Both players play a hand
        p1_hand_score = simulate_hand(p1_x)
        p2_hand_score = simulate_hand(p2_x)

        new_p1 = p1_score + p1_hand_score
        new_p2 = p2_score + p2_hand_score

        # Check terminal conditions
        p1_won = new_p1 >= WIN_THRESHOLD
        p2_won = new_p2 >= WIN_THRESHOLD

        if p1_won and p2_won:
            # Both crossed - higher score wins
            if new_p1 > new_p2:
                wins += 1
            elif new_p1 == new_p2:
                wins += 0.5  # Tie counts as half win
            # else: P2 wins
        elif p1_won:
            wins += 1
        elif p2_won:
            pass  # P2 wins
        else:
            # Neither won - look up win probability from new state
            new_p1_rounded = round_to_10(new_p1)
            new_p2_rounded = round_to_10(new_p2)
            wins += win_probs.get((new_p1_rounded, new_p2_rounded), 0.5)

    return wins / n_sims


def compute_optimal_strategies():
    """
    Use backwards induction to compute optimal strategies for all states.

    Returns:
        optimal_strategies: dict mapping (p1_score, p2_score) -> best X for P1
        win_probs: dict mapping (p1_score, p2_score) -> P1 win probability
    """
    optimal_strategies = {}
    win_probs = {}

    # Generate all states, sorted by sum of scores (descending) for backwards induction
    all_states = [(p1, p2) for p1 in SCORE_STEPS for p2 in SCORE_STEPS]
    all_states.sort(key=lambda s: s[0] + s[1], reverse=True)

    print(f"Computing optimal strategies for {len(all_states)} states...")
    print(f"Testing {len(X_VALUES)} strategy values with {SIMS_PER_STRATEGY} simulations each")

    for p1_score, p2_score in tqdm(all_states, desc="Backwards induction"):
        best_x = 0
        best_win_rate = -1

        # For each possible P1 strategy, find best response
        for p1_x in X_VALUES:
            # P2 uses their optimal strategy for the symmetric position
            # (opponent's perspective: their score is p2_score, opponent has p1_score)
            p2_x = optimal_strategies.get((p2_score, p1_score), 25)  # Default to ~optimal single-hand

            win_rate = evaluate_strategy(
                p1_score, p2_score, p1_x, p2_x,
                win_probs, optimal_strategies, SIMS_PER_STRATEGY
            )

            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_x = p1_x

        optimal_strategies[(p1_score, p2_score)] = best_x
        win_probs[(p1_score, p2_score)] = best_win_rate

    return optimal_strategies, win_probs


def save_results(optimal_strategies, win_probs):
    """Save results to data directory."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # Convert tuple keys to strings for JSON serialization
    results = {
        "optimal_strategies": {f"{k[0]},{k[1]}": v for k, v in optimal_strategies.items()},
        "win_probs": {f"{k[0]},{k[1]}": v for k, v in win_probs.items()},
        "parameters": {
            "x_values": X_VALUES,
            "score_steps": SCORE_STEPS,
            "sims_per_strategy": SIMS_PER_STRATEGY,
            "win_threshold": WIN_THRESHOLD
        }
    }

    filepath = os.path.join(DATA_DIR, "multisim_results.json")
    with open(filepath, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {filepath}")
    return filepath


def load_results():
    """Load results from data directory."""
    filepath = os.path.join(DATA_DIR, "multisim_results.json")

    with open(filepath, "r") as f:
        data = json.load(f)

    # Convert string keys back to tuples
    optimal_strategies = {}
    for k, v in data["optimal_strategies"].items():
        p1, p2 = map(int, k.split(","))
        optimal_strategies[(p1, p2)] = v

    win_probs = {}
    for k, v in data["win_probs"].items():
        p1, p2 = map(int, k.split(","))
        win_probs[(p1, p2)] = v

    return optimal_strategies, win_probs, data["parameters"]


def main():
    print("Flip7 Multi-Player Strategy Optimizer")
    print("=" * 50)

    optimal_strategies, win_probs = compute_optimal_strategies()
    save_results(optimal_strategies, win_probs)

    # Print summary
    print("\nSample optimal strategies:")
    sample_states = [(0, 0), (100, 100), (150, 100), (100, 150), (190, 190)]
    for state in sample_states:
        if state in optimal_strategies:
            print(f"  State {state}: STRAT({optimal_strategies[state]}), "
                  f"P1 win prob: {win_probs[state]:.2%}")


if __name__ == "__main__":
    main()
