for year in {2025..2029}
do
    python3 -m src.league_mgmt.league --season $year \
        --competition_constant $(echo "1.0 + 0.1 * ($year - 2025)" | bc)
done