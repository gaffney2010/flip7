# strategy_learnings.py

STRATEGY_ANALYSIS = """
<div class="learnings">
    <h2>Strategic Insights</h2>

    <h3>1. Relative Position Dominates Absolute Score</h3>
    <p>
        A striking pattern emerges from the heatmap: optimal strategy is governed almost entirely by the
        <strong>score differential</strong> between players, not their absolute positions. Whether the game
        stands at 20-40 or 120-140, the strategic calculus remains remarkably similar. This invariance
        suggests that Flip7 strategy reduces to a one-dimensional problem: how far ahead or behind you are.
    </p>
    <p>
        The diagonal bands of consistent color across the heatmap make this visually apparent—cells along
        any diagonal (constant difference) tend toward the same threshold value.
    </p>

    <h3>2. Calibrated Aggression: A Threshold Guide</h3>
    <p>
        The optimal threshold follows an intuitive gradient based on your position relative to your opponent:
    </p>
    <ul>
        <li><strong>Comfortable lead (70+ points ahead):</strong> Play conservatively at <strong>threshold 10</strong>.
            With a substantial buffer, there's no need to risk a bust. Take what the deck gives you and
            protect your advantage.</li>
        <li><strong>Moderate lead (20-70 points ahead):</strong> Use <strong>threshold 20</strong>.
            You can afford to be slightly more selective while still avoiding unnecessary risk.</li>
        <li><strong>Even game:</strong> The equilibrium strategy sits at <strong>threshold 30</strong>—the same
            value that maximizes expected single-hand score. When neither player has an edge, play for
            optimal expected value.</li>
        <li><strong>Moderate deficit (20-40 points behind):</strong> Increase aggression to <strong>threshold 40</strong>.
            You need above-average hands to close the gap, which requires accepting higher bust risk.</li>
        <li><strong>Significant deficit (50+ points behind):</strong> Pursue the <strong>Flip 7 bonus</strong>
            aggressively. When conventional play can't bridge the gap, your best path to victory runs through
            the distribution's upper tail—the ~60-point hands that only materialize when you draw all seven cards.
            This is the "long tail" phenomenon from our single-hand analysis now deployed as a strategic weapon.</li>
    </ul>
    <p>
        This framework transforms a complex 400-cell decision matrix into a simple heuristic: assess your
        deficit (or surplus), and adjust your risk tolerance accordingly.
    </p>
</div>
"""
