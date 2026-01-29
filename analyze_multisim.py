"""
analyze_multisim.py - Generate heatmap visualization of optimal Flip7 strategies.

Creates an HTML page with a heatmap showing the optimal STRAT(X) for player 1
at each game state (player_score, opponent_score).
"""

import os
from jinja2 import Template

from multisim import load_results, SCORE_STEPS


def get_color(value):
    """Generate color from blue (low) to red (high) for X values 0-100."""
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

    # Generate color map for all possible X values (0-100 by 5s)
    colors = {x: get_color(x) for x in range(0, 101, 5)}
    # Also add intermediate values in case they appear
    for x in range(0, 101):
        if x not in colors:
            colors[x] = get_color(x)

    # Load and render template
    with open("strategy_heatmap.html.j2", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        strategies=optimal_strategies,
        colors=colors,
        score_steps=SCORE_STEPS,
        sims_per_strategy=params["sims_per_strategy"]
    )

    os.makedirs("out", exist_ok=True)
    output_path = "out/strategy_heatmap.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Analysis complete. Heatmap saved to {output_path}")


if __name__ == "__main__":
    main()
