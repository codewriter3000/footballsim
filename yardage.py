def get_yardage_on_run_play(net_run):
    if   net_run < 0.01:
        return -5
    elif net_run < 0.02:
        return -4
    elif net_run < 0.03:
        return -3
    elif net_run < 0.04:
        return -2
    elif net_run < 0.24:
        return -1
    elif net_run < 0.40:
        return 0
    elif net_run < 0.62:
        return 1
    elif net_run < 0.90:
        return 2
    elif net_run < 1.10:
        return 3
    elif net_run < 1.34:
        return 4
    elif net_run < 1.46:
        return 5
    elif net_run < 1.58:
        return 6
    elif net_run < 1.64:
        return 7
    elif net_run < 1.68:
        return 8
    elif net_run < 1.72:
        return 9
    elif net_run < 1.76:
        return 10
    elif net_run < 1.80:
        return 11
    elif net_run < 1.82:
        return 12
    elif net_run < 1.84:
        return 13
    elif net_run < 1.86:
        return 14
    elif net_run < 1.88:
        return 15
    elif net_run < 1.90:
        return 16
    elif net_run < 1.91:
        return 17
    elif net_run < 1.92:
        return 18
    elif net_run < 1.93:
        return 19
    elif net_run < 1.94:
        return 20
    elif net_run < 1.95:
        return 21
    elif net_run < 1.96:
        return 22
    elif net_run < 1.97:
        return 23
    else:
        return 100

def get_yardage_on_pass_play(net_pass):
    if   net_pass < 0.76:
        return 'INCOMPLETE'
    elif net_pass < 0.78:
        return 1
    elif net_pass < 0.80:
        return 2
    elif net_pass < 0.84:
        return 3
    elif net_pass < 0.92:
        return 4
    elif net_pass < 1.02:
        return 5
    elif net_pass < 1.10:
        return 6
    elif net_pass < 1.20:
        return 7
    elif net_pass < 1.30:
        return 8
    elif net_pass < 1.40:
        return 9
    elif net_pass < 1.45:
        return 10
    elif net_pass < 1.50:
        return 11
    elif net_pass < 1.60:
        return 12
    elif net_pass < 1.70:
        return 13
    elif net_pass < 1.75:
        return 14
    elif net_pass < 1.80:
        return 15
    elif net_pass < 1.85:
        return 16
    elif net_pass < 1.86:
        return 17
    elif net_pass < 1.87:
        return 18
    elif net_pass < 1.88:
        return 19
    elif net_pass < 1.89:
        return 20
    elif net_pass < 1.90:
        return 21
    elif net_pass < 1.91:
        return 22
    elif net_pass < 1.92:
        return 23
    elif net_pass < 1.93:
        return 24
    elif net_pass < 1.94:
        return 25
    elif net_pass < 1.95:
        return 26
    elif net_pass < 1.96:
        return 27
    elif net_pass < 1.97:
        return 28
    elif net_pass < 1.98:
        return 29
    elif net_pass < 1.99:
        return 30
    else:
        return 100


