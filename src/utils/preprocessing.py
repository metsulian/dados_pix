from datetime import datetime

def prepare_data(data):
    for row in data:
        row["AnoMes"] = datetime.strptime(str(row["AnoMes"]), "%Y%m").date()
    return data

def show_values(x):
    if (x >= 10**3 and x < 10**6) or (x <= -10**3 and x > -10**6):
        return (f'{round(x / 10**3, 2)} Mil')
    elif (x >= 10**6 and x < 10**9) or (x <= -10**6 and x > -10**9):
        return(f'{round(x / 10**6, 2)} Milhões')
    elif (x >= 10**9 and x < 10**12) or (x <= -10**9 and x > -10**12):
        return(f'{round(x / 10**9, 2)} Bilhões')
    elif x >= 10**12 or x <= -10**12:
        return(f'{round(x / 10**12, 2)} Trilhões')
    return (f'{round(x, 2)}')