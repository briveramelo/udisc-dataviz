def get_color(hole_score: int):
    p_p2 = 'rgba(255, 50, 50, 0.3)'
    p_p1 = 'rgba(255, 150, 0, 0.3)'
    p_p0 = 'rgba(100, 100, 100, 0.3)'
    p_m1 = 'rgba(20, 20, 255, 0.3)'
    p_m2 = 'rgba(50, 255, 50, 1)'
    p_m3 = 'rgba(255, 0, 255, 1)'

    color = p_p2
    if hole_score >= 2:
        color = p_p2
    elif hole_score == 1:
        color = p_p1
    elif hole_score == 0:
        color = p_p0
    elif hole_score == -1:
        color = p_m1
    elif hole_score == -2:
        color = p_m2
    elif hole_score <= -3:
        color = p_m3

    return color


def normalize(val: float, min: float, max: float):
    result = (val - min) / (max - min)
    if result == 0:
        return 0.001  # plotly has a reported rendering error when normalized values == 0 or 1
    if result == 1:
        return 0.999
    return result
