import random
from util import verbose_print

from yardage import get_yardage_on_run_play, get_yardage_on_pass_play

team_1 = {
    'offense': {
        'LT':   80,
        'LG':   80,
        'C':    80,
        'RG':   80,
        'RT':   80,
        'Q':    80,
        'H':    80,
        'X':    80,
        'F':    80,
        'Y':    80,
        'Z':    80,
    },
    'defense': {
        'LE':   80,
        'DT1':  80,
        'DT2':  80,
        'RE':   80,
        'SLB':  80,
        'WLB':  80,
        'MLB':  80,
        'SCB':  80,
        'WCB':  80,
        'FS':   80,
        'SS':   80, 
    }
}

team_2 = {
    'offense': {
        'LT':   80,
        'LG':   80,
        'C':    80,
        'RG':   80,
        'RT':   80,
        'Q':    80,
        'H':    80,
        'X':    80,
        'F':    80,
        'Y':    80,
        'Z':    80,
    },
    'defense': {
        'LE':   80,
        'DT1':  80,
        'DT2':  80,
        'RE':   80,
        'SLB':  80,
        'WLB':  80,
        'MLB':  80,
        'SCB':  80,
        'WCB':  80,
        'FS':   80,
        'SS':   80, 
    }
}

def fourth_down_logic(distance, yard_line):
    if yard_line < 50:
        return 'PUNT'
    if yard_line < 60 and distance > 10:
        return 'PUNT'
    if distance > 5:
        return 'FIELD GOAL'
    return 'GO FOR IT'

def play_football_game(team1, team2):
    quarter = [1,]
    seconds = [900,]
    team1_points = [0,]
    team2_points = [0,]
    yard_line = [25,]

    while True:
        run_drive(team1['offense'], team2['defense'], quarter, seconds, yard_line, team1_points, team2_points)

        yard_line[0] = 100 - yard_line[0]
        if quarter[0] % 2 == 0 and seconds[0] <= 0:
            verbose_print(f'TEAM 1: {team1_points[0]}')
            verbose_print(f'TEAM 2: {team2_points[0]}')
            if quarter[0] == 2:
                verbose_print('END OF HALF')
                quarter[0] += 1
                seconds[0] = 900
            else:
                verbose_print('FINAL')
                return {'Team 1': team1_points[0], 'Team 2': team2_points[0]}

        run_drive(team2['offense'], team1['defense'], quarter, seconds, yard_line, team2_points, team1_points)

        yard_line[0] = 100 - yard_line[0]
        if quarter[0] % 2 == 0 and seconds[0] <= 0:
            verbose_print(f'TEAM 1: {team1_points[0]}')
            verbose_print(f'TEAM 2: {team2_points[0]}')
            if quarter[0] == 2:
                verbose_print('END OF HALF')
                quarter[0] += 1
                seconds[0] = 900
            else:
                verbose_print('FINAL')
                return {'Team 1': team1_points[0], 'Team 2': team2_points[0]}

def run_drive(offense, defense, quarter_t, seconds_t, yard_line_t, off_points_t, def_points_t):
    down = 1
    distance = 10

    while True:
        if yard_line_t[0] < 0:
            verbose_print('SAFETY')
            def_points_t[0] += 2
            yard_line_t[0] = 65
            return

        verbose_print(' ')
        verbose_print(f'DOWN: {down}')
        verbose_print(f'DISTANCE: {distance}')
        verbose_print(f'YARDLINE: {yard_line_t[0]}')
        verbose_print(f'QUARTER: {quarter_t[0]}')
        verbose_print(f'TIME: {seconds_t[0]//60}:{seconds_t[0]%60:02d}')

        # Time between plays
        seconds_t[0] -= random.randint(25, 35)

        if seconds_t[0] <= 0:
            if quarter_t[0]%2 == 1:
                verbose_print(f'END OF QUARTER')
                quarter_t[0] += 1
                seconds_t[0] = 900
            else:
                return

        # 4th down logic
        if down == 4:
            if fourth_down_logic(distance, yard_line_t[0]) == 'FIELD GOAL':
                verbose_print('FIELD GOAL IS GOOD')
                seconds_t[0] -= random.randint(3, 4)
                off_points_t[0] += 3
                yard_line_t[0] = 75
                return

            if fourth_down_logic(distance, yard_line_t[0]) == 'PUNT':
                verbose_print('PUNT')
                seconds_t[0] -= random.randint(5, 10)
                yard_line_t[0] += random.randint(40, 70)

                if yard_line_t[0] >= 100:
                    yard_line_t[0] = 75

                return

        play_result = run_play(offense, defense)
        seconds_t[0] -= play_result['play_time']

        if play_result['event'] == 'INTERCEPTION':
            verbose_print('INTERCEPTION')
            return
        
        net_yards = play_result['net_yards']
        if net_yards + yard_line_t[0] >= 100:
            verbose_print('TOUCHDOWN')
            off_points_t[0] += 7
            yard_line_t[0] = 75
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
        
        yard_line_t[0] += net_yards

def run_play(offense, defense):
    oline_strength = (offense['LT'] + offense['LG'] + offense['C'] + offense['RG'] + offense['RT'])/5
    receiver_strength = (offense['X'] + offense['F'] + offense['Y'] + offense['Z'])/4

    running_o_strength = (oline_strength*5 + (offense['Q'] + offense['H'])*2)/7

    dline_strength = (defense['LE'] + defense['DT1'] + defense['DT2'] + defense['RE']) / 4
    lb_strength = (defense['SLB'] + defense['MLB'] + defense['WLB']) / 3
    db_strength = (defense['SCB'] + defense['WCB'] + defense['FS'] + defense['SS']) / 4

    running_d_strength = (dline_strength*4 + lb_strength*3)/7
    passing_d_strength = (db_strength*4 + lb_strength*3)/7

    offensive_play_type = 'run' if random.randint(1, 2) % 2 == 0 else 'pass'
    defensive_play_type = 'base' if random.randint(1, 2) % 2 == 0 else 'blitz'

    # 0.0 = worst outcome for offense, 2.0 = best outcome for offense
    outcome = random.uniform(0, 2)

    play_time = random.randint(4, 6)

    if offensive_play_type == 'run':
        net_run = outcome# * running_o_strength / running_d_strength

        net_yards = get_yardage_on_run_play(net_run)

        return {
                'event': 'RUN',
                'play_time': play_time,
                'net_yards': net_yards,
            }

    elif offensive_play_type == 'pass':
        pass_protection_coefficient = dline_strength / oline_strength
        sack_chance = random.uniform(0, 1.1) * pass_protection_coefficient

        net_pass = outcome

        net_yards = get_yardage_on_pass_play(net_pass)

        if sack_chance >= 1:
            net_yards = random.randint(-15, -1)
            return {
                    'event': 'SACK',
                    'play_time': play_time,
                    'net_yards': net_yards,
                }

        interception_coefficient = db_strength / offense['Q']
        interception_chance = random.uniform(0, 1.02) * interception_coefficient

        if interception_chance >= 1:
            return {
                    'event': 'INTERCEPTION',
                    'play_time': random.randint(4, 12),
                }

        if net_yards == 'INCOMPLETE':
            return {
                    'event': 'INCOMPLETE',
                    'play_time': play_time,
                    'net_yards': 0,
                }
        else:
            return {
                    'event': 'PASS COMPLETE',
                    'play_time': random.randint(4, 12),
                    'net_yards': net_yards,
                }

play_football_game(team_1, team_2)
