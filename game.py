import random
from dataclasses import dataclass

from util import verbose_print
from yardage import get_yardage_on_run_play, get_yardage_on_pass_play

# ----- GAME / CLOCK SETTINGS -----
PLAY_CLOCK_MIN = 25
PLAY_CLOCK_MAX = 35

QUARTER_LENGTH = 900
KICKOFF_YARDLINE = 25
SAFETY_FREE_KICK_YARDLINE = 65

# ----- SCORING -----
TOUCHDOWN_POINTS = 7
FIELD_GOAL_POINTS = 3
SAFETY_POINTS = 2

# ----- FOURTH DOWN LOGIC -----
PUNT_NO_MATTER_YARDLINE = 50
PUNT_LONG_FG_YARDLINE = 60
LONG_FG_DISTANCE = 10
FG_TOO_LONG_DISTANCE = 5

# ----- PUNT / FG RESULTS -----
FG_TIME_MIN = 3
FG_TIME_MAX = 4

PUNT_TIME_MIN = 5
PUNT_TIME_MAX = 10

PUNT_DISTANCE_MIN = 40
PUNT_DISTANCE_MAX = 70

TOUCHBACK_YARDLINE = 75

# ----- PLAY RESULTS -----
RUN_PLAY_TIME_MIN = 4
RUN_PLAY_TIME_MAX = 6

PASS_PLAY_TIME_MIN = 4
PASS_PLAY_TIME_MAX = 12

SACK_YARDS_MIN = -15
SACK_YARDS_MAX = -1

# ----- PASS RISK / PROBABILITY -----
SACK_CHANCE_MULTIPLIER = 1.1
INTERCEPTION_CHANCE_MULTIPLIER = 1.02

# ----- PLAY OUTCOME DISTRIBUTION -----
OUTCOME_MIN = 0.0
OUTCOME_MAX = 2.0
OUTCOME_MODE = 0.98

# ----- BLITZ EFFECTS -----
BLITZ_BAD_OUTCOME_MULTIPLIER = 0.95
BLITZ_GOOD_OUTCOME_MULTIPLIER = 1.05
BLITZ_RUN_EXPONENT = 1.5
O_LINE_BLITZ_MULTIPLIER = 1.2
OUTCOME_BLITZ_MULTIPLIER = 1.05


@dataclass
class GameState:
    quarter: int = 1
    seconds: int = QUARTER_LENGTH
    yard_line: int = KICKOFF_YARDLINE
    team1_points: int = 0
    team2_points: int = 0


def fourth_down_logic(distance: int, yard_line: int) -> str:
    if yard_line < PUNT_NO_MATTER_YARDLINE:
        return 'PUNT'
    if yard_line < PUNT_LONG_FG_YARDLINE and distance > LONG_FG_DISTANCE:
        return 'PUNT'
    if distance > FG_TOO_LONG_DISTANCE:
        return 'FIELD GOAL'
    return 'GO FOR IT'


def handle_period_end(state: GameState) -> bool:
    if state.quarter % 2 == 0 and state.seconds <= 0:
        verbose_print(f'TEAM 1: {state.team1_points}')
        verbose_print(f'TEAM 2: {state.team2_points}')
        if state.quarter == 2:
            verbose_print('END OF HALF')
            state.quarter += 1
            state.seconds = QUARTER_LENGTH
            return False
        else:
            verbose_print('FINAL')
            return True
    return False


def play_football_game(team1, team2):
    state = GameState()

    while True:
        run_drive(team1['offense'], team2['defense'], state, True)
        state.yard_line = 100 - state.yard_line

        if handle_period_end(state):
            return {'Team 1': state.team1_points, 'Team 2': state.team2_points}

        run_drive(team2['offense'], team1['defense'], state, False)
        state.yard_line = 100 - state.yard_line

        if handle_period_end(state):
            return {'Team 1': state.team1_points, 'Team 2': state.team2_points}


def run_drive(offense, defense, state: GameState, offense_is_team1: bool):
    down = 1
    distance = 10

    while True:
        if state.yard_line < 0:
            verbose_print('SAFETY')
            if offense_is_team1:
                state.team2_points += SAFETY_POINTS
            else:
                state.team1_points += SAFETY_POINTS
            state.yard_line = SAFETY_FREE_KICK_YARDLINE
            return

        verbose_print(' ')
        verbose_print(f'DOWN: {down}')
        verbose_print(f'DISTANCE: {distance}')
        verbose_print(f'YARDLINE: {state.yard_line}')
        verbose_print(f'QUARTER: {state.quarter}')
        verbose_print(f'TIME: {state.seconds // 60}:{state.seconds % 60:02d}')

        state.seconds -= random.randint(PLAY_CLOCK_MIN, PLAY_CLOCK_MAX)

        if state.seconds <= 0:
            if state.quarter % 2 == 1:
                verbose_print('END OF QUARTER')
                state.quarter += 1
                state.seconds = QUARTER_LENGTH
            else:
                return

        if down == 4:
            decision = fourth_down_logic(distance, state.yard_line)

            if decision == 'FIELD GOAL':
                verbose_print('FIELD GOAL IS GOOD')
                state.seconds -= random.randint(FG_TIME_MIN, FG_TIME_MAX)
                if offense_is_team1:
                    state.team1_points += FIELD_GOAL_POINTS
                else:
                    state.team2_points += FIELD_GOAL_POINTS
                state.yard_line = TOUCHBACK_YARDLINE
                return

            if decision == 'PUNT':
                verbose_print('PUNT')
                state.seconds -= random.randint(PUNT_TIME_MIN, PUNT_TIME_MAX)
                state.yard_line += random.randint(PUNT_DISTANCE_MIN, PUNT_DISTANCE_MAX)
                if state.yard_line >= 100:
                    state.yard_line = TOUCHBACK_YARDLINE
                return

        play_result = run_play(offense, defense)
        state.seconds -= play_result['play_time']

        event = play_result['event']
        net_yards = play_result.get('net_yards', 0)

        if event == 'INTERCEPTION':
            verbose_print('INTERCEPTION')
            return

        if net_yards + state.yard_line >= 100:
            verbose_print('TOUCHDOWN')
            if offense_is_team1:
                state.team1_points += TOUCHDOWN_POINTS
            else:
                state.team2_points += TOUCHDOWN_POINTS
            state.yard_line = TOUCHBACK_YARDLINE
            return

        if net_yards > distance:
            verbose_print('FIRST DOWN')
            down = 1
            distance = 10
        else:
            if down == 4:
                verbose_print('TURNOVER ON DOWNS')
                return
            down += 1
            distance -= net_yards

        state.yard_line += net_yards


def run_play(offense, defense):
    oline_strength = (offense['LT'] + offense['LG'] + offense['C'] +
                      offense['RG'] + offense['RT']) / 5

    running_o_strength = (oline_strength * 5 + (offense['Q'] + offense['H']) * 2) / 7

    dline_strength = (defense['LE'] + defense['DT1'] +
                      defense['DT2'] + defense['RE']) / 4
    lb_strength = (defense['SLB'] + defense['MLB'] + defense['WLB']) / 3
    db_strength = (defense['SCB'] + defense['WCB'] +
                   defense['FS'] + defense['SS']) / 4

    running_d_strength = (dline_strength * 4 + lb_strength * 3) / 7

    offensive_play_type = random.choice(('run', 'pass'))
    defensive_play_type = random.choice(('base', 'blitz'))

    outcome = random.triangular(OUTCOME_MIN, OUTCOME_MAX, OUTCOME_MODE)
    if defensive_play_type == 'blitz':
        outcome = outcome * BLITZ_BAD_OUTCOME_MULTIPLIER if outcome < 1.15 else outcome * BLITZ_GOOD_OUTCOME_MULTIPLIER

    play_time = random.randint(RUN_PLAY_TIME_MIN, RUN_PLAY_TIME_MAX)

    if offensive_play_type == 'run':
        diff_in_line_strength = running_o_strength - running_d_strength
        net_run = outcome + (diff_in_line_strength / 1000)
        if defensive_play_type == 'blitz':
            net_run = net_run ** BLITZ_RUN_EXPONENT

        net_yards = get_yardage_on_run_play(net_run)
        return {'event': 'RUN', 'play_time': play_time, 'net_yards': net_yards}

    # PASS
    if defensive_play_type == 'blitz':
        dline_strength *= O_LINE_BLITZ_MULTIPLIER
        outcome *= OUTCOME_BLITZ_MULTIPLIER

    pass_protection = dline_strength / oline_strength
    sack_chance = random.uniform(0, SACK_CHANCE_MULTIPLIER) * pass_protection

    if sack_chance >= 1:
        net_yards = random.randint(SACK_YARDS_MIN, SACK_YARDS_MAX)
        return {'event': 'SACK', 'play_time': play_time, 'net_yards': net_yards}

    net_pass = outcome
    net_yards = get_yardage_on_pass_play(net_pass)

    interception_coeff = db_strength / offense['Q']
    interception_chance = random.uniform(0, INTERCEPTION_CHANCE_MULTIPLIER) * interception_coeff

    if interception_chance >= 1:
        return {'event': 'INTERCEPTION', 'play_time': random.randint(PASS_PLAY_TIME_MIN, PASS_PLAY_TIME_MAX)}

    if net_yards == 'INCOMPLETE':
        return {'event': 'INCOMPLETE', 'play_time': play_time, 'net_yards': 0}

    return {'event': 'PASS COMPLETE',
            'play_time': random.randint(PASS_PLAY_TIME_MIN, PASS_PLAY_TIME_MAX),
            'net_yards': net_yards}

