import os
import re
import statistics
import plotly.graph_objects as go
from jinja2 import Template
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

    # 1. Create Line Graph Figure
    fig_lines = go.Figure()
    fig_lines.add_trace(go.Scatter(x=valid_strategies, y=avg_scores, name="Average Score", mode='lines+markers'))
    fig_lines.add_trace(go.Scatter(x=valid_strategies, y=median_scores, name="Median Score", mode='lines+markers'))
    fig_lines.update_layout(
        title="Average and Median Scores vs Strategy X",
        xaxis_title="Strategy Threshold (X)",
        yaxis_title="Score",
        height=450
    )

    # 2. Create Histogram Figure with Slider
    fig_hist = go.Figure()
    for i, x in enumerate(valid_strategies):
        fig_hist.add_trace(
            go.Histogram(
                x=all_scores_by_x[x],
                name=f"X={x}",
                visible=(i == 0),
                nbinsx=30,
                marker_color='blue'
            )
        )

    steps = []
    for i, x in enumerate(valid_strategies):
        visibility = [False] * len(valid_strategies)
        visibility[i] = True
        steps.append(dict(
            method="update",
            args=[{"visible": visibility}, {"title": f"Score Distribution (Histogram): X={x}"}],
            label=str(x)
        ))

    fig_hist.update_layout(
        sliders=[dict(active=0, currentvalue={"prefix": "Strategy X: "}, pad={"t": 50}, steps=steps)],
        height=500,
        title=f"Score Distribution (Histogram): X={valid_strategies[0]}",
        xaxis_title="Score Value",
        yaxis_title="Frequency"
    )

    # 3. Render with Jinja2
    with open("learnings.html.j2", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        line_graph_div=fig_lines.to_html(full_html=False, include_plotlyjs=False),
        hist_graph_div=fig_hist.to_html(full_html=False, include_plotlyjs=False)
    )

    os.makedirs("out", exist_ok=True)
    with open("out/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Analysis complete. Results saved to out/index.html")

if __name__ == "__main__":
    main()
