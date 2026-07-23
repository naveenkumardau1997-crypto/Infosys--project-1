risk_score = 0
events = []


def add_event(event, points):
    global risk_score

    risk_score += points

    events.append({
        "event": event,
        "points": points
    })


def get_score():
    return risk_score


def get_events():
    return events


def get_risk_level():

    if risk_score <= 2:
        return "LOW"

    elif risk_score <= 5:
        return "MEDIUM"

    return "HIGH"


def reset():
    global risk_score, events
    risk_score = 0
    events = []