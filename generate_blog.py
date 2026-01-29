"""
generate_blog.py - Generate the Flip7 strategy analysis blog post.

Combines data from single-hand simulations and game-theoretic analysis
into a comprehensive blog post with interactive visualizations.
"""

import os
import re
import statistics

import plotly.graph_objects as go
from jinja2 import Template

from sim import read_simulations, DATA_DIR
from multisim import load_results, SCORE_STEPS


def get_available_strategies():
    """Finds all X values that have simulation data in the data directory."""
    strategies = []
    if not os.path.exists(DATA_DIR):
        return strategies
    for filename in os.listdir(DATA_DIR):
        match = re.match(r"sim_results_(\d+)\.jsonl", filename)
        if match:
            strategies.append(int(match.group(1)))
    return sorted(strategies)


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
    # Load single-hand simulation data
    strategies = get_available_strategies()
    if not strategies:
        print(f"No simulation data found in {DATA_DIR}/. Run run_sims.sh first.")
        return

    avg_scores = []
    median_scores = []
    all_scores_by_x = {}
    valid_strategies = []

    print(f"Loading single-hand simulation data for {len(strategies)} strategies...")
    for x in strategies:
        scores = [res["total_value"] for res in read_simulations(x)]
        if scores:
            valid_strategies.append(x)
            avg_scores.append(statistics.mean(scores))
            median_scores.append(statistics.median(scores))
            all_scores_by_x[x] = scores

    if not valid_strategies:
        print("No valid scores found in simulation files.")
        return

    # Create Line Graph
    print("Creating line graph...")
    fig_lines = go.Figure()
    fig_lines.add_trace(go.Scatter(
        x=valid_strategies,
        y=avg_scores,
        name="Average Score",
        mode='lines+markers',
        line=dict(color='#3498db', width=2),
        marker=dict(size=6)
    ))
    fig_lines.add_trace(go.Scatter(
        x=valid_strategies,
        y=median_scores,
        name="Median Score",
        mode='lines+markers',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=6)
    ))
    fig_lines.update_layout(
        title="Average and Median Scores vs Strategy Threshold",
        xaxis_title="Strategy Threshold (X)",
        yaxis_title="Score",
        height=450,
        font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#eee'),
        yaxis=dict(gridcolor='#eee')
    )

    # Create Histogram with Slider
    print("Creating histogram with slider...")
    fig_hist = go.Figure()
    for i, x in enumerate(valid_strategies):
        fig_hist.add_trace(
            go.Histogram(
                x=all_scores_by_x[x],
                name=f"X={x}",
                visible=(i == 0),
                nbinsx=30,
                marker_color='#3498db'
            )
        )

    steps = []
    for i, x in enumerate(valid_strategies):
        visibility = [False] * len(valid_strategies)
        visibility[i] = True
        steps.append(dict(
            method="update",
            args=[{"visible": visibility}, {"title": f"Score Distribution: Threshold X = {x}"}],
            label=str(x)
        ))

    fig_hist.update_layout(
        sliders=[dict(
            active=0,
            currentvalue={"prefix": "Strategy X: "},
            pad={"t": 50},
            steps=steps
        )],
        height=500,
        title=f"Score Distribution: Threshold X = {valid_strategies[0]}",
        xaxis_title="Score",
        yaxis_title="Frequency",
        font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#eee'),
        yaxis=dict(gridcolor='#eee')
    )

    # Load game-theoretic analysis data
    print("Loading game-theoretic analysis data...")
    try:
        optimal_strategies, win_probs, params = load_results()
    except FileNotFoundError:
        print("No multisim results found. Run multisim.py first.")
        return

    # Process strategies - mark hopeless situations as N/A
    processed_strategies = {}
    for key, strategy in optimal_strategies.items():
        if strategy == 0:
            processed_strategies[key] = None  # N/A
        else:
            processed_strategies[key] = strategy

    # Generate color map
    colors = {x: get_color(x) for x in range(0, 101)}
    colors[None] = get_color(None)

    # Load and render template
    print("Rendering blog post...")
    with open("blog_post.html.j2", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        line_graph_div=fig_lines.to_html(full_html=False, include_plotlyjs=False),
        hist_graph_div=fig_hist.to_html(full_html=False, include_plotlyjs=False),
        strategies=processed_strategies,
        colors=colors,
        score_steps=SCORE_STEPS
    )

    os.makedirs("out", exist_ok=True)
    output_path = "out/blog_post.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Blog post generated successfully: {output_path}")


if __name__ == "__main__":
    main()
