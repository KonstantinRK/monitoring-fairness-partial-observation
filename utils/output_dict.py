

def get_output_dict(lower_bound, upper_bound, point_estimate, true_value):
    return {"verdict_lower": lower_bound, "verdict_upper": upper_bound, "point_estimate": point_estimate,
            "true_value": true_value}