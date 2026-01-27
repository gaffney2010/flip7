# learnings.py

ANALYSIS_SUMMARY = """
<div style="font-family: sans-serif; max-width: 1000px; margin: 20px auto; line-height: 1.6; color: #333;">
    <h2>Strategic Insights</h2>
    
    <h3>1. Expected Value and the 'Sweet Spot'</h3>
    <p>
        The <strong>Average Score</strong> curve exhibits a smooth, concave profile, reaching its zenith in the <strong>X = 25–30</strong> range. 
        This represents the optimal strategic threshold for maximizing long-term expected value, where the marginal utility of 
        additional points is perfectly balanced against the escalating risk of a bust.
    </p>

    <h3>2. The Median Phase Transition</h3>
    <p>
        The <strong>Median Score</strong> demonstrates a linear relationship (y ≈ x) with the strategy threshold until approximately 
        <strong>X = 35</strong>. At this critical juncture, the cumulative probability of busting crosses the 50% threshold, 
        causing the median to collapse abruptly to zero. This indicates a sharp phase transition from "likely scoring" to 
        "likely busting."
    </p>

    <h3>3. Distribution Dynamics</h3>
    <p>
        The histograms reveal a classic risk-reward trade-off: as X increases, the distribution shifts toward higher values at 
        the cost of a significantly heavier weight at zero. Notably, the non-bust distribution tends to cluster tightly 
        just above the threshold X, suggesting minimal "overshoot" once the standing condition is met.
    </p>

    <h3>4. The 'Flip 7' Long Tail</h3>
    <p>
        A distinct "long tail" persists around the <strong>60-point mark</strong>. This represents the <strong>Flip 7 bonus</strong> 
        scenario (successfully drawing 7 cards). While this occurs in only ~1% of trials at low X, its frequency increases to 
        roughly 10% as X approaches infinity. In high-threshold strategies, this "Flip 7" path becomes the primary—and 
        eventually only—surviving non-zero component of the distribution.
    </p>
</div>
"""
