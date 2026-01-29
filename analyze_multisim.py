"""
analyze_multisim.py - Generate heatmap visualization of optimal Flip7 strategies.

Creates an HTML page with a heatmap showing the optimal strategy threshold for player 1
at each game state (player_score, opponent_score).
"""

import os
from jinja2 import Template

from multisim import load_results, SCORE_STEPS
from strategy_learnings import STRATEGY_ANALYSIS


def get_color(value):
    """Generate color from blue (low) to red (high) for X values 0-100."""
    if value is None:
        return "rgb(200, 200, 200)"  # Gray for N/A
    ratio = value / 100
    r = int(59 + ratio * (231 - 59))
    g = int(130 + ratio * (76 - 130))
    b = int(246 + ratio * (60 - 246))
    return f"rgb({r}, {g}, {b})"


def main():
    # Load results
    try:
        optimal_strategies, win_probs, params = load_results()
    except FileNotFoundError:
        print("No multisim results found. Run multisim.py first.")
        return

    # Process strategies - mark hopeless situations as N/A
    # If X=0 is "optimal" but win probability is low, all strategies performed
    # similarly poorly, so mark as N/A (strategy doesn't matter)
    processed_strategies = {}
    for key, strategy in optimal_strategies.items():
        win_prob = win_probs.get(key, 0)
        if strategy == 0:
            processed_strategies[key] = None  # N/A - all strategies equally ineffective
        else:
            processed_strategies[key] = strategy

    # Generate color map for all possible X values (0-100)
    colors = {x: get_color(x) for x in range(0, 101)}
    colors[None] = get_color(None)  # For N/A

    # Load and render template
    with open("strategy_heatmap.html.j2", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        strategies=processed_strategies,
        colors=colors,
        score_steps=SCORE_STEPS,
        sims_per_strategy=params["sims_per_strategy"],
        strategy_analysis=STRATEGY_ANALYSIS
    )

    os.makedirs("out", exist_ok=True)
    output_path = "out/strategy_heatmap.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Analysis complete. Heatmap saved to {output_path}")


if __name__ == "__main__":
    main()
