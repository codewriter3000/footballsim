import random
import statistics
import sys
import os

def generate_ratings(median=75, stdev=7.5, minimum=50, maximum=99):
    offense_positions = [
        "LT", "LG", "C", "RG", "RT",
        "Q", "H", "X", "F", "Y", "Z"
    ]

    defense_positions = [
        "LE", "DT1", "DT2", "RE",
        "SLB", "WLB", "MLB",
        "SCB", "WCB", "FS", "SS"
    ]

    total_positions = len(offense_positions) + len(defense_positions)

    # Generate values from a normal distribution and clamp to range
    raw = []
    for _ in range(total_positions):
        val = int(random.gauss(median, stdev))
        val = max(minimum, min(maximum, val))  # clamp
        raw.append(val)

    # Shuffle ratings for randomness
    random.shuffle(raw)

    # Assign ratings to positions
    offense = {pos: raw[i] for i, pos in enumerate(offense_positions)}
    defense = {pos: raw[i + len(offense_positions)] for i, pos in enumerate(defense_positions)}

    return {
        "offense": offense,
        "defense": defense
    }

if __name__ == '__main__':
    file_path = sys.argv[1]
    print(file_path)

    with open(file_path, 'w') as file:
        file.write(str(generate_ratings()))

