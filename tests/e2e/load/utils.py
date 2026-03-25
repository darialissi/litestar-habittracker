import numpy as np


def percentile(values: list[float], percent: int) -> float:
    if not values:
        return 0.0
    return float(np.percentile(values, percent))
