import random
import statistics
import sys
import os
import json


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


def write_single_team(file_path: str):
    """Original behavior: write one team ratings JSON to a specific file."""
    random_rating = random.randint(65, 85)
    ratings = generate_ratings(median=random_rating)
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(ratings, file, indent=2)
    print(f"Wrote single team ratings to {file_path}")


def bulk_generate_teams(names_file: str, output_dir: str = "teams"):
    """
    Bulk mode: read team names line-by-line from names_file and
    generate one JSON ratings file per team in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(names_file, "r", encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if not name:
                continue  # skip empty lines

            ratings = generate_ratings()
            filename = os.path.join(output_dir, f"{name}.json")

            with open(filename, "w", encoding="utf-8") as out:
                json.dump(ratings, out, indent=2)

            print(f"Generated team '{name}' -> {filename}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single team: python generate_ratings.py output.json")
        print("  Bulk teams : python generate_ratings.py --bulk names.txt [output_dir]")
        sys.exit(1)

    if sys.argv[1] == "--bulk":
        if len(sys.argv) < 3:
            print("Usage: python generate_ratings.py --bulk names.txt [output_dir]")
            sys.exit(1)

        names_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) >= 4 else "teams"
        bulk_generate_teams(names_file, output_dir)
    else:
        # Original behavior: first arg is a single output file path
        file_path = sys.argv[1]
        write_single_team(file_path)

