def grade(state):
    total = len(state["tickets"])
    resolved = sum(t["resolved"] for t in state["tickets"])
    sla_ok = sum(1 for t in state["tickets"] if t["sla"] >= 0)
    satisfaction = state["satisfaction"]

    score = (
        0.5 * (resolved / total) +
        0.3 * (sla_ok / total) +
        0.2 * satisfaction
    )

    return round(min(score, 1.0), 3)