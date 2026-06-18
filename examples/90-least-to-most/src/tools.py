# Problems chosen for least-to-most because they require chained multi-step
# arithmetic where each step depends on the previous result.
# Unlike single-pass CoT, least-to-most forces explicit sub-question sequencing.

SAMPLE_PROBLEMS = [
    (
        "A baker makes 3 batches of cookies per hour. Each batch yields 24 cookies. "
        "The baker works 4.5 hours and sells 2/3 of all cookies at $0.75 each. "
        "How much money does the baker earn?"
    ),
    (
        "A company has 3 departments: Engineering (40 people), Marketing (25 people), "
        "and Sales (35 people). 20% of Engineering, 40% of Marketing, and 60% of Sales "
        "work remotely. What percentage of the total company works remotely?"
    ),
    (
        "A car travels at 60 mph for the first half of a journey (by distance) "
        "and 40 mph for the second half. What is the car's average speed for "
        "the entire journey?"
    ),
]
