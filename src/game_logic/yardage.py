import bisect

run_thresholds = [
    0.01, 0.02, 0.03, 0.04, 0.24, 0.40, 0.62,
    0.90, 1.10, 1.34, 1.46, 1.58, 1.64, 1.68,
    1.72, 1.76, 1.80, 1.82, 1.84, 1.86, 1.88,
    1.90, 1.91, 1.92, 1.93, 1.94, 1.95, 1.96, 1.97
]

run_values = [
    -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
    19, 20, 21, 22, 23
]

def get_yardage_on_run_play(net_run):
    idx = bisect.bisect_left(run_thresholds, net_run)
    return run_values[idx] if idx < len(run_values) else 100

pass_thresholds = [
    0.76, 0.78, 0.80, 0.84, 0.92, 1.02, 1.10, 1.20,
    1.30, 1.40, 1.45, 1.50, 1.60, 1.70, 1.75, 1.80,
    1.85, 1.86, 1.87, 1.88, 1.89, 1.90, 1.91, 1.92,
    1.93, 1.94, 1.95, 1.96, 1.97, 1.98, 1.99
]

pass_values = [
    "INCOMPLETE", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
    26, 27, 28, 29, 30
]

def get_yardage_on_pass_play(net_pass):
    idx = bisect.bisect_left(pass_thresholds, net_pass)
    return pass_values[idx] if idx < len(pass_values) else 100

