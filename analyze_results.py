import os
import re
import statistics
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sim import read_simulations, DATA_DIR

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

def main():
    strategies = get_available_strategies()
    if not strategies:
        print(f"No simulation data found in {DATA_DIR}/. Run run_sims.sh first.")
        return

    avg_scores = []
    median_scores = []
    all_scores_by_x = {}
    valid_strategies = []

    print(f"Processing data for {len(strategies)} strategies...")
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

    # Create Subplots: Top for Line Graphs, Bottom for Histogram
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Average and Median Scores vs Strategy X", "Score Distribution (Histogram)"),
        vertical_spacing=0.15
    )

    # 1. Line Graphs (Average and Median)
    fig.add_trace(
        go.Scatter(x=valid_strategies, y=avg_scores, name="Average Score", mode='lines+markers'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=valid_strategies, y=median_scores, name="Median Score", mode='lines+markers'),
        row=1, col=1
    )

    # 2. Histogram with Slider
    # Add a histogram trace for every strategy; only the first one is visible initially
    for i, x in enumerate(valid_strategies):
        fig.add_trace(
            go.Histogram(
                x=all_scores_by_x[x],
                name=f"X={x}",
                visible=(i == 0),
                nbinsx=30,
                marker_color='blue'
            ),
            row=2, col=1
        )

    # Create Slider steps
    steps = []
    for i, x in enumerate(valid_strategies):
        # Visibility list: [Line1, Line2, Hist_0, Hist_1, ..., Hist_i, ..., Hist_N]
        # The first two traces (Line Graphs) are always visible.
        visibility = [True, True] + [False] * len(valid_strategies)
        visibility[i + 2] = True
        
        step = dict(
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Flip7 Strategy Analysis (Current Histogram: X={x})"}],
            label=str(x)
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Strategy X: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
        height=900,
        title_text="Flip7 Strategy Analysis",
        showlegend=True,
        xaxis_title="Strategy Threshold (X)",
        yaxis_title="Score",
        xaxis2_title="Score Value",
        yaxis2_title="Frequency"
    )

    # Ensure output directory exists
    os.makedirs("out", exist_ok=True)
    output_file = "out/index.html"
    fig.write_html(output_file)
    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
